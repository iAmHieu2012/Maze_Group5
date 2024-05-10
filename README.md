-Khởi động:	
	Username, password
	Nút login, reset
	Create account:
		Sign up page:
			Username, password, confirm -> sign up
	Trả về: giao diện
-Giao diện:
	Play
		Chọn level:
			Easy
			Medium
			Hard
		Chọn chế độ chơi:
			Bình thường
			SPEEDRUN
			Giới hạn bước đi
	Trả về màn hình game
		
	Autoplay
		Chọn level:
			Easy
			Medium
			Hard
		Chọn chế độ chơi:
			Bình thường
			SPEEDRUN
			Giới hạn bước đi
		Trả về màn hình game
		
	Leaderboard
		Đọc file leaderboard.txt

	Loadgame
		Đọc file seved_game.txt
		Chọn game
		Trả về màn hình game đã lưu


	Setting
		Set_background: 1,2
		Sound: điều chỉnh âm thanh to nhỏ
			Âm thanh có âm thanh bên ngoài & trong khi chơi

	About
	Instruction
	Logout:
		2 tuỳ chọn: yes, no

-	Chơi game:
	Hiển thị:
		Bình thường:
			Thời gian
		Speedrun:
			Thời gian đếm ngược
		Giới hạn bước đi:
			Số bước đi đếm ngược
			
	Bắt đầu:
		Đặt Tom và điểm đích ở 2 vị trí ngẫu nhiên sao cho 2 điểm này cách 			nhau 1 khoảng nhất định

	Sử dụng phím mũi tên để di chuyển
	Dừng: bấm nút Esc
		Khi bấm nút esc:
			Dừng thời gian
			Hiển thị dialog (chú ý che hết map)
			Các nút bấm:
				Chơi tiếp
				Điều chỉnh âm thanh
	Kết thúc:
		Bình thường:
			So sánh thời gian, hiển thị kỷ lục nếu có
		Speedrun:
			Thắng:
				Hiển thị màn hình thắng
				So sánh với kỷ lục  hiển thị kỷ lục nếu có
			Thua:
				Thông báo màn hình thua

		Giới hạn bước đi:
			Thắng: hiển thị màn hình thắng
			Thua: hiển thị màn hình thua
		
		Hiển thị tuỳ chọn chơi lại
			Nếu có:
				Trả về bắt đầu chơi game
			Không:
				Quay lại menu
		




