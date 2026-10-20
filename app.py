import random
import time
import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="Chung Kết World Cup: Argentina vs Pháp",
    page_icon="⚽",
    layout="centered",
)

st.title("⚽ World Cup Final: Argentina vs Pháp")
st.caption("Tái hiện loạt sút luân lưu cân não đỉnh cao!")

# 1. Khởi tạo trạng thái trò chơi
if "game_started" not in st.session_state:
  st.session_state.game_started = False
if "my_team" not in st.session_state:
  st.session_state.my_team = "Argentina"
if "score" not in st.session_state:
  st.session_state.score = {"Argentina": 0, "Pháp": 0}
if "kicks" not in st.session_state:
  st.session_state.kicks = {"Argentina": 0, "Pháp": 0}
if "history" not in st.session_state:
  st.session_state.history = []
if "current_turn" not in st.session_state:
  st.session_state.current_turn = "Argentina"
if "game_over" not in st.session_state:
  st.session_state.game_over = False

# Màn hình chọn đội bóng
if not st.session_state.game_started:
  st.subheader("Chọn đội bóng bạn muốn điều khiển:")
  col_team1, col_team2 = st.columns(2)

  with col_team1:
    if st.button("🇦🇷 Điều khiển Argentina", use_container_width=True):
      st.session_state.my_team = "Argentina"
      st.session_state.opponent_team = "Pháp"
      st.session_state.game_started = True
      st.rerun()

  with col_team2:
    if st.button("🇫🇷 Điều khiển Pháp", use_container_width=True):
      st.session_state.my_team = "Pháp"
      st.session_state.opponent_team = "Argentina"
      st.session_state.game_started = True
      st.rerun()

else:
  # 2. Hiển thị bảng tỷ số
  col1, col2, col3 = st.columns([2, 1, 2])
  with col1:
    st.markdown(f"### 🇦🇷 Argentina: **{st.session_state.score['Argentina']}**")
    st.write(f"Số lượt sút: {st.session_state.kicks['Argentina']}/5")
  with col2:
    st.markdown("## VS")
  with col3:
    st.markdown(f"### 🇫🇷 Pháp: **{st.session_state.score['Pháp']}**")
    st.write(f"Số lượt sút: {st.session_state.kicks['Pháp']}/5")

  st.divider()

  # 3. Xử lý logic khi game chưa kết thúc
  if not st.session_state.game_over:
    turn = st.session_state.current_turn
    is_player_turn = turn == st.session_state.my_team

    if is_player_turn:
      st.subheader(f"🎯 Lượt sút của bạn ({turn})")
      st.write("Chọn góc bạn muốn thực hiện cú sút:")

      col_l, col_c, col_r = st.columns(3)
      shoot_dir = None

      if col_l.button("⬅️ Trái", key="shoot_left", use_container_width=True):
        shoot_dir = "Trái"
      if col_c.button("⬆️ Giữa", key="shoot_center", use_container_width=True):
        shoot_dir = "Giữa"
      if col_r.button("➡️ Phải", key="shoot_right", use_container_width=True):
        shoot_dir = "Phải"

      if shoot_dir:
        # Thủ môn đối phương đoán hướng ngẫu nhiên
        gk_dir = random.choice(["Trái", "Giữa", "Phải"])

        with st.spinner("Cầu thủ đang lấy đà... 🏃💨"):
          time.sleep(1)

        st.session_state.kicks[turn] += 1
        if shoot_dir != gk_dir:
          st.session_state.score[turn] += 1
          st.balloons()
          st.success(
              f"⚽ **VÀÔÔÔ!** Bạn sút góc **{shoot_dir}**, thủ môn bay người"
              f" **{gk_dir}**!"
          )
          st.session_state.history.append(
              f"✅ {turn}: Sút VÀO góc {shoot_dir} (GK bay {gk_dir})"
          )
        else:
          st.error(
              f"❌ **CẢN PHÁ TUYỆT VỜI!** Thủ môn đã đoán đúng góc **{gk_dir}**!"
          )
          st.session_state.history.append(
              f"❌ {turn}: Sút HỎNG góc {shoot_dir} (GK cản phá)"
          )

        # Đổi lượt sút
        st.session_state.current_turn = st.session_state.opponent_team
        time.sleep(1.5)
        st.rerun()

    else:
      st.subheader(f"🛡️ Đối phương ({turn}) đang sút luân lưu!")
      st.write("Hãy chọn hướng đổ người của thủ môn:")

      col_l, col_c, col_r = st.columns(3)
      save_dir = None

      if col_l.button(
          "⬅️ Bay Trái", key="save_left", use_container_width=True
      ):
        save_dir = "Trái"
      if col_c.button(
          "⬆️ Đứng Giữa", key="save_center", use_container_width=True
      ):
        save_dir = "Giữa"
      if col_r.button(
          "➡️ Bay Phải", key="save_right", use_container_width=True
      ):
        save_dir = "Phải"

      if save_dir:
        # Máy sút ngẫu nhiên
        bot_shoot_dir = random.choice(["Trái", "Giữa", "Phải"])

        with st.spinner("Cầu thủ đối phương dang sút... ⚽"):
          time.sleep(1)

        st.session_state.kicks[turn] += 1
        if save_dir == bot_shoot_dir:
          st.success(
              f"🧤 **CẢN PHÁ THÀNH CÔNG!** Đối phương sút góc"
              f" **{bot_shoot_dir}** và bạn đã đoán đúng!"
          )
          st.session_state.history.append(
              f"🧤 Thủ môn cản phá cú sút của {turn} (Góc {bot_shoot_dir})"
          )
        else:
          st.session_state.score[turn] += 1
          st.error(
              f"⚽ **VÀO!** {turn} sút góc **{bot_shoot_dir}**, bạn đổ người góc"
              f" **{save_dir}**."
          )
          st.session_state.history.append(
              f"⚽ {turn}: Sút VÀO góc {bot_shoot_dir}"
          )

        # Đổi lượt sút
        st.session_state.current_turn = st.session_state.my_team
        time.sleep(1.5)
        st.rerun()

    # Kiểm tra điều kiện kết thúc (sau 5 lượt sút mỗi đội)
    k_arg = st.session_state.kicks["Argentina"]
    k_fra = st.session_state.kicks["Pháp"]
    s_arg = st.session_state.score["Argentina"]
    s_fra = st.session_state.score["Pháp"]

    if k_arg >= 5 and k_fra >= 5:
      if s_arg != s_fra:
        st.session_state.game_over = True
      else:
        # Nếu hòa thì đá tiếp knock-out từng lượt
        st.info("⚡ Hai đội đang hòa! Bắt đầu lượt sút sinh tử (Sudden Death)!")

  # 4. Màn hình tổng kết khi trò chơi kết thúc
  else:
    s_arg = st.session_state.score["Argentina"]
    s_fra = st.session_state.score["Pháp"]

    if s_arg > s_fra:
      winner = "Argentina 🏆"
      st.snow()
    else:
      winner = "Pháp 🏆"
      st.balloons()

    st.header(f"🎉 CHÚC MỪNG {winner} ĐÃ VÔ ĐỊCH WORLD CUP!")
    st.write(f"Tỷ số chung cuộc: **Argentina {s_arg} - {s_fra} Pháp**")

    if st.button("🔄 Chơi lại trận đấu mới", use_container_width=True):
      st.session_state.game_started = False
      st.session_state.score = {"Argentina": 0, "Pháp": 0}
      st.session_state.kicks = {"Argentina": 0, "Pháp": 0}
      st.session_state.history = []
      st.session_state.current_turn = "Argentina"
      st.session_state.game_over = False
      st.rerun()

  # 5. Nhật ký các lượt sút
  st.divider()
  with st.expander("📜 Lịch sử các lượt sút penalty"):
    for log in reversed(st.session_state.history):
      st.write(log)
