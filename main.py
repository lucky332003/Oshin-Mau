# ============================================================
# 🧑‍💻 Tác giả: Thành ( HADES )
# 📅 Mô tả: Bot Discord cho phép người dùng chọn màu role bằng mã HEX
#          và tự động xoá role nếu không còn ai sử dụng.
# ============================================================

import discord
from discord.ext import commands
from discord import app_commands, ui
import os

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🎨 Danh sách 20 màu preset
COLOR_PRESETS = {
    "🔴 Đỏ": "FF0000",
    "🟠 Cam": "FFA500",
    "🟡 Vàng": "FFFF00",
    "🟢 Xanh lá": "00FF00",
    "🔵 Xanh dương": "0000FF",
    "🟣 Tím": "800080",
    "⚫ Đen": "000000",
    "⚪ Trắng": "FFFFFF",
    "🟤 Nâu": "8B4513",
    "🌸 Hồng nhạt": "FFC0CB",
    "💗 Hồng đậm": "FF69B4",
    "🌊 Xanh nước biển": "4682B4",
    "🌿 Xanh rêu": "556B2F",
    "🌞 Vàng nghệ": "FFD700",
    "💎 Xanh ngọc": "00CED1",
    "🧊 Xanh da trời": "87CEEB",
    "🍇 Tím nho": "9932CC",
    "🌋 Cam đất": "FF4500",
    "🐚 Be nhạt": "F5F5DC",
    "🪨 Xám tro": "A9A9A9"
}

class HexModal(ui.Modal, title="🔧 Nhập mã HEX tuỳ chỉnh"):
    hex_input = ui.TextInput(label="Mã màu HEX (VD: #FF5733)", placeholder="#000000", max_length=7)

    async def on_submit(self, interaction: discord.Interaction):
        hex_code = self.hex_input.value.strip().lstrip("#").upper()
        if len(hex_code) != 6 or any(c not in "0123456789ABCDEF" for c in hex_code):
            await interaction.response.send_message("❌ Mã HEX không hợp lệ!", ephemeral=True)
            return
        await assign_color_role(interaction, hex_code)

class ColorView(ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(ColorSelect())
        self.add_item(OpenHexButton())

class ColorSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=hex_code, description=f"Mã HEX: #{hex_code}")
            for name, hex_code in COLOR_PRESETS.items()
        ]
        super().__init__(placeholder="🎨 Chọn màu từ danh sách", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        hex_code = self.values[0]
        await assign_color_role(interaction, hex_code)

class OpenHexButton(ui.Button):
    def __init__(self):
        super().__init__(label="💡 Nhập mã HEX tuỳ chỉnh", style=discord.ButtonStyle.primary, custom_id="open_hex_button")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(HexModal())

async def assign_color_role(interaction: discord.Interaction, hex_code: str):
    guild = interaction.guild
    member = interaction.user

    # ❌ Xoá role cũ của user nếu là role màu
    for role in member.roles:
        if role.name.upper().startswith("#") or (len(role.name) == 6 and all(c in "0123456789ABCDEF" for c in role.name.upper())):
            try:
                await member.remove_roles(role)
                if not role.members:
                    await role.delete(reason=f"Role màu #{role.name} không còn ai sử dụng")
            except Exception:
                pass

    # ✅ Tạo hoặc lấy role mới theo HEX
    role_name = hex_code
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(
            name=role_name,
            colour=discord.Colour(int(hex_code, 16)),
            reason=f"Tạo màu role cho {member.name}"
        )
        bot_top = guild.me.top_role
        await guild.edit_role_positions({role: bot_top.position - 1})

    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ Đã gán màu `#{hex_code}` thành công!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Bot không thể gán role. Kiểm tra quyền và thứ tự role.", ephemeral=True)

@bot.tree.command(
    name="chonmau",
    description="🎨 Chọn hoặc nhập màu HEX để tạo role cá nhân (Tác giả: Thành - HADES)"
)
async def chonmau(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🎨 **Chọn màu hoặc nhập mã HEX bên dưới**\nTác giả: **Thành ( HADES )**",
        view=ColorView(),
        ephemeral=True
    )

@bot.tree.command(
    name="tudongxoarole",
    description="🧹 Dọn dẹp role màu không còn ai sử dụng (Tác giả: Thành - HADES)"
)
@app_commands.checks.has_permissions(manage_roles=True)
async def tudongxoarole(interaction: discord.Interaction):
    await interaction.response.send_message("🧹 **Đang xoá các role màu không còn ai sử dụng...**\nTác giả: **Thành ( HADES )**", ephemeral=True)
    
    guild = interaction.guild
    deleted_roles = []

    for role in guild.roles:
        if len(role.name) == 6 and all(c in "0123456789ABCDEF" for c in role.name.upper()):
            if not role.members:
                try:
                    await role.delete(reason="Không còn ai sử dụng role màu này")
                    deleted_roles.append(role.name)
                except Exception:
                    pass

    if deleted_roles:
        role_list = ", ".join(f"`#{r}`" for r in deleted_roles)
        await interaction.followup.send(f"✅ Đã xoá các role không dùng nữa: {role_list}", ephemeral=True)
    else:
        await interaction.followup.send("✅ Không có role nào cần xoá.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot đã sẵn sàng với tên: {bot.user}")

# Lấy token từ biến môi trường
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ Lỗi: Không tìm thấy DISCORD_TOKEN trong biến môi trường.")