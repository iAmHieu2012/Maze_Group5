import pygame
import json

# Hàm để đọc dữ liệu từ tệp JSON
def read_accounts_from_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file is not found
    except json.JSONDecodeError:
        return {}  # Return an empty dictionary if there's an error parsing the JSON

# Hàm để kiểm tra tài khoản đăng nhập hoặc đăng kí có tồn tại trong file json trước đó hay không
def check_account(username, password, accounts):
    if username in accounts.keys():
        if accounts[username] == password:
            return True
    return False

# Hàm để kiểm tra username có tồn tại trong file json trước đó hay không
def check_username(username, password, accounts):
    if username in accounts.keys():
        return True
    return False

# Hàm thêm tài khoản đăng kí
def add_account(filename, username, password):
    data = read_accounts_from_json(filename)
    data[username] = password
    with open(filename, "w") as f:
        json.dump(data, f, indent = 4)

def login():
    # Định nghĩa màu sắc
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 191, 255)
    RED = (255, 0, 0)

    # Tạo font chữ
    font_1 = pygame.font.Font(None, 36)
    font_2 = pygame.font.Font(None, 30)
    font_3 = pygame.font.Font(None, 24)

    # Biến lưu trữ tên người dùng
    username_input = ""
    password_input = ""

    # Đặt cờ hiệu input hiện tại là username hay là password
    current_input = "None"

    # đặt cờ hiệu flag, nếu đăng nhập sai thì đổi thành false
    flag = None

    # Biến xác định vị trí ô vuông bên cạnh username, ô vuông bên cạnh password, ô Login và ô Reset
    username_rect = pygame.Rect(600, screen_height // 2 - font_2.get_height() // 2 - 50 - 10, 170, font_2.get_height() + 10) #username thuộc font_2 
    password_rect = pygame.Rect(600, screen_height // 2 - font_2.get_height() // 2 - 10, 170, font_2.get_height() + 10) #password thuộc font_2
    Login_rect = pygame.Rect(485 - 5, screen_height // 2 - font_3.get_height() // 2 + 50 - 10, 55, font_3.get_height() + 10) #Login thuộc font_3
    Reset_rect = pygame.Rect(585 - 5, screen_height // 2 - font_3.get_height() // 2 + 50 - 10, 55, font_3.get_height() + 10) #reset thuộc font_3
    createnewaccount_rect = pygame.Rect(480, screen_height // 2 - font_1.get_height() // 2 + 175, 230, font_2.get_height() + 10) #reset thuộc font_3

    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
    def is_over_username_box(mouse_pos):
        return username_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh password hay không
    def is_over_password_box(mouse_pos):
        return password_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô Login hay không
    def is_over_Login_box(mouse_pos):
        return Login_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô Reset hay không
    def is_over_Reset_box(mouse_pos):
        return Reset_rect.collidepoint(mouse_pos)
    def is_over_CreateNewAccount_box(mouse_pos):
        return createnewaccount_rect.collidepoint(mouse_pos)

    blink_timer = 0
    blink_interval = 60  # Điều chỉnh khoảng thời gian nhấp nháy

    # Vòng lặp chính
    running = True
    while running:
        # Cập nhật timer của dấu nháy
        blink_timer += 1
        if blink_timer >= blink_interval:
            blink_timer = 0

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Thoát khỏi pygame khi nhấn nút tắt màn hình
                quit()  # Thoát khỏi chương trình
            # Bắt sự kiện nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
                if is_over_username_box(mouse_pos):
                    current_input = "username"
                if is_over_password_box(mouse_pos):
                    current_input = "password"
                if is_over_Reset_box(mouse_pos):
                    username_input = ""
                    password_input = ""
                    current_input = "None"
                if is_over_CreateNewAccount_box(mouse_pos):
                    return sign_up()
                if is_over_Login_box(mouse_pos):
                    filename = 'accounts.json'
                    # Đọc dữ liệu từ tệp JSON
                    accounts = read_accounts_from_json(filename)
                    # Xử lý sự kiện đăng nhập
                    if check_account(username_input, password_input, accounts):
                        flag = True
                        # khi ráp code thì return ra username_input
                        running = False
                        return username_input
                    else:
                        # Đăng nhập không thành công, đặt cờ hiệu không thành công
                        flag = False
            # Bắt sự kiện nhập văn bản vào ô username or password
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_input == "username":
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong username
                        username_input = username_input[:-1]
                    elif current_input == "password":
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong password
                        password_input = password_input[:-1]
                elif event.key == pygame.K_RETURN:
                    current_input = "None"
                # phần thêm vào chức năng điều khiển nút up down
                elif event.key == pygame.K_UP:
                    if current_input == "None":
                        current_input = "password"
                    elif current_input == "username":
                        current_input = "password"
                    elif current_input == "password":
                        current_input = "username"
                elif event.key == pygame.K_DOWN: 
                    if current_input == "None":
                        current_input = "username"
                    elif current_input == "username":
                        current_input = "password"
                    elif current_input == "password":
                        current_input = "username"                           
                else:
                    if current_input == "username":
                        if len(username_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào username
                            username_input += event.unicode
                        else:
                            # nếu độ dài bằng 20 thì lấy 20 kí tự cuối cùng
                            username_input += event.unicode
                            username_input = username_input[1:]
                    elif current_input == "password":
                        if len(password_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào password
                            password_input += event.unicode
                        else:
                            password_input += event.unicode
                            password_input = password_input[1:]                 

        # Tô màu màn hình
        screen.fill(WHITE)

        # Render và vẽ các thành phần giao diện
        loginpage = font_1.render("Login Page", True, BLACK, WHITE)
        if current_input == "None":
            username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            password = font_2.render(f"Password     {'*' * len(password_input)}", True, BLACK, WHITE)       
        elif current_input == "username":
            password = font_2.render(f"Password     {'*' * len(password_input)}", True, BLACK, WHITE)
            if blink_timer < blink_interval / 2:
                username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            else:
                username = font_2.render(f"Username    {'*' * len(username_input)}|", True, BLACK, WHITE)
        elif current_input == "password":
            username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            if blink_timer < blink_interval / 2:
                password = font_2.render(f"Password     {'*' * len(password_input)}", True, BLACK, WHITE)
            else:
                password = font_2.render(f"Password     {'*' * len(password_input)}|", True, BLACK, WHITE)

        Login = font_3.render("Login", True, BLACK, WHITE)
        Reset = font_3.render("Reset", True, BLACK, WHITE)
        donthaveaccount = font_2.render("Don't have account ?", True, BLACK, WHITE)
        createnewaccount = font_2.render("Create New Account !!!", True, BLUE, WHITE)
        login_fail = font_3.render("Invalid username or password!", True, RED, WHITE)  # Khi đăng nhập không thành công
        login_success = font_3.render("Login successful !", True, RED, WHITE)  # Khi đăng nhập thành công


        #Vẽ đối tượng văn bản lên màn hình ở vị trí mong muốn
        screen.blit(loginpage, (screen_width // 2 - loginpage.get_width() // 2, screen_height // 2 - loginpage.get_height() // 2 - 125))
        screen.blit(username, (480, screen_height // 2 - loginpage.get_height() // 2 - 50))
        screen.blit(password, (480, screen_height // 2 - loginpage.get_height() // 2))
        screen.blit(Login, (485, screen_height // 2 - loginpage.get_height() // 2 + 50))
        screen.blit(Reset, (585, screen_height // 2 - loginpage.get_height() // 2 + 50))
        screen.blit(donthaveaccount, (480, screen_height // 2 - loginpage.get_height() // 2 + 125))
        screen.blit(createnewaccount, (480, screen_height // 2 - loginpage.get_height() // 2 + 175))
        if flag == True:
            screen.blit(login_success, (675, screen_height // 2 - loginpage.get_height() // 2 + 50)) # Khi đăng nhập thành công
        elif flag == False:
            screen.blit(login_fail, (675, screen_height // 2 - loginpage.get_height() // 2 + 50)) # Khi đăng nhập không thành công

        # Vẽ hình chữ nhật xung quanh vùng nhập dữ liệu, ô login, ô reset
        pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - username.get_height() // 2 - 50 - 10, 170, username.get_height() + 10), 2)
        pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - password.get_height() // 2 - 10, 170, password.get_height() + 10), 2)
        pygame.draw.rect(screen, BLACK, (485 - 5, screen_height // 2 - Login.get_height() // 2 + 50 - 10 , 55, Login.get_height() + 10), 2)
        pygame.draw.rect(screen, BLACK, (585 - 5, screen_height // 2 - Reset.get_height() // 2 + 50 - 10, 55, Reset.get_height() + 10), 2)
        #pygame.draw.rect(screen, BLACK, (480 - 5, screen_height // 2 - loginpage.get_height() // 2 + 175 - 5, 230, createnewaccount.get_height() + 10), 2)
      
        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(60)

    # Thoát khỏi Pygame
    #pygame.quit()

def sign_up():
 
    # Định nghĩa màu sắc
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 191, 255)
    RED = (255, 0, 0)

    # Tạo font chữ
    font_1 = pygame.font.Font(None, 36)
    font_2 = pygame.font.Font(None, 30)
    font_3 = pygame.font.Font(None, 24)
    font_4 = pygame.font.Font(None, 18)

    # Biến lưu trữ tên người dùng
    username_input = ""
    password_1_input = ""
    password_2_input = ""

    # Đặt cờ hiệu input hiện tại là username hay là password
    current_input = "None"

    # Đặt cờ hiệu sign up có thành công hay không
    flag_password = None
    flag_account = None
    flag_username = None

    # Biến xác định vị trí ô vuông bên cạnh username, ô vuông bên cạnh password, ô signup
    username_rect = pygame.Rect(600, screen_height // 2 - font_2.get_height() // 2 - 50 - 10, 170, font_2.get_height() + 10) #username thuộc font_2 
    password_1_rect = pygame.Rect(600, screen_height // 2 - font_2.get_height() // 2 - 10, 170, font_2.get_height() + 10) #password thuộc font_2
    password_2_rect = pygame.Rect(600, screen_height // 2 - font_2.get_height() // 2 + 50 - 10, 170, font_2.get_height() + 10) #password thuộc font_2
    signup_rect = pygame.Rect(485 - 5, screen_height // 2 - font_3.get_height() // 2 + 100 - 10, 70, font_3.get_height() + 10) #Login thuộc font_3

    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
    def is_over_username_box(mouse_pos):
        return username_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh password1 hay không
    def is_over_password_1_box(mouse_pos):
        return password_1_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh password2 hay không
    def is_over_password_2_box(mouse_pos):
        return password_2_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô signup
    def is_over_signup_box(mouse_pos):
        return signup_rect.collidepoint(mouse_pos)

    blink_timer = 0
    blink_interval = 60  # Điều chỉnh khoảng thời gian nhấp nháy

    # Vòng lặp chính
    running = True
    while running:
        # Cập nhật timer của dấu nháy
        blink_timer += 1
        if blink_timer >= blink_interval:
            blink_timer = 0
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Thoát khỏi pygame khi nhấn nút tắt màn hình
                quit()  # Thoát khỏi chương trình
            # Bắt sự kiện nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
                if is_over_username_box(mouse_pos):
                    current_input = "username"
                if is_over_password_1_box(mouse_pos):
                    current_input = "password_1"
                if is_over_password_2_box(mouse_pos):
                    current_input = "password_2"
                if is_over_signup_box(mouse_pos):
                    # Lưu ý, cho phép đăng kí mới True, còn không cho phép thì False, chưa biết thì None
                    if password_1_input != password_2_input:
                        flag_password = False
                        flag_account = None
                        flag_username = None
                        password_1_input = ""
                        password_2_input = ""                        
                    else:
                        flag_password = True
                        filename = "accounts.json"
                        accounts = read_accounts_from_json(filename)
                        if check_account(username_input, password_1_input, accounts):
                            # nếu đã tồn tại thì không cho phép sign up
                            flag_account = False
                            flag_username = None
                            username_input = ""
                            password_1_input = ""
                            password_2_input = ""
                        else: # không tồn tại tài khoản nhưng có thể trùng username
                            flag_account = True
                            if check_username(username_input, password_1_input, accounts):
                                flag_username = False
                                username_input = ""  
                            else:                
                                add_account(filename, username_input, password_1_input)
                                flag_account = True
                                # nếu ráp code muốn return ra chuỗi username mới thì return ngay chỗ này
                                running = False  
                                print(username_input)  
                                return username_input                    
          
            # Bắt sự kiện nhập văn bản vào ô username or password
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_input == "username":
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong username
                        username_input = username_input[:-1]
                    elif current_input == "password_1":
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong password
                        password_1_input = password_1_input[:-1]
                    elif current_input == "password_2":
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong password
                        password_2_input = password_2_input[:-1]
                elif event.key == pygame.K_RETURN:
                    current_input = "None"
                elif event.key == pygame.K_UP:
                    if current_input == "None":
                        current_input = "password_2"
                    elif current_input == "username":
                        current_input = "password_2"
                    elif current_input == "password_1":
                        current_input = "username"
                    elif current_input == "password_2":
                        current_input = "password_1"
                elif event.key == pygame.K_DOWN:
                    if current_input == "None":
                        current_input = "username"
                    elif current_input == "username":
                        current_input = "password_1"
                    elif current_input == "password_1":
                        current_input = "password_2"
                    elif current_input == "password_2":
                        current_input = "username"                    
                else:
                    if current_input == "username":
                        if len(username_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào username
                            username_input += event.unicode
                        else:
                            # nếu độ dài bằng 20 thì lấy 20 kí tự cuối cùng
                            username_input += event.unicode
                            username_input = username_input[1:]
                    elif current_input == "password_1":
                        if len(password_1_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào password
                            password_1_input += event.unicode
                        else:
                            password_1_input += event.unicode
                            password_1_input = password_1_input[1:]                 
                    elif current_input == "password_2":
                        if len(password_2_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào password
                            password_2_input += event.unicode
                        else:
                            password_2_input += event.unicode
                            password_2_input = password_2_input[1:]                 


        # Tô màu màn hình
        screen.fill(WHITE)
        # Render và vẽ các thành phần giao diện

        signuppage = font_1.render("Sign up Page", True, BLACK, WHITE)
        if current_input == "None":
            username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, BLACK, WHITE)
            password_2 = font_2.render(f"Confirm        {'*' * len(password_2_input)}", True, BLACK, WHITE)     
        elif current_input == "username":
            password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, BLACK, WHITE)
            password_2 = font_2.render(f"Confirm        {'*' * len(password_2_input)}", True, BLACK, WHITE)
            if blink_timer < blink_interval / 2:
                username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            else:
                username = font_2.render(f"Username    {'*' * len(username_input)}|", True, BLACK, WHITE)
        elif current_input == "password_1":
            username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            password_2 = font_2.render(f"Confirm        {'*' * len(password_2_input)}", True, BLACK, WHITE)
            if blink_timer < blink_interval / 2:
                password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, BLACK, WHITE)
            else:
                password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}|", True, BLACK, WHITE)
        elif current_input == "password_2":
            username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
            password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, BLACK, WHITE)
            if blink_timer < blink_interval / 2:
                password_2 = font_2.render(f"Confirm        {'*' * len(password_2_input)}", True, BLACK, WHITE)
            else:
                password_2 = font_2.render(f"Confirm        {'*' * len(password_2_input)}|", True, BLACK, WHITE)

        # username = font_2.render(f"Username    {'*' * len(username_input)}", True, BLACK, WHITE)
        # password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, BLACK, WHITE)
        # password_2 = font_2.render(f"Confirm        {'*' * len(password_2_input)}", True, BLACK, WHITE)

        signup = font_3.render("Sign up", True, BLACK, WHITE)
        wrong_password = font_3.render("Please check your password again !", True, RED, WHITE)
        existed_account = font_3.render("This account has been existed, please create a new account !", True, RED, WHITE)
        existed_username = font_3.render("This username has been existed, please create a new username !", True, RED, WHITE)

        #Vẽ đối tượng văn bản lên màn hình ở vị trí mong muốn
        screen.blit(signuppage, (screen_width // 2 - signuppage.get_width() // 2, screen_height // 2 - signuppage.get_height() // 2 - 125))
        screen.blit(username, (480, screen_height // 2 - signuppage.get_height() // 2 - 50))
        screen.blit(password_1, (480, screen_height // 2 - signuppage.get_height() // 2))
        screen.blit(password_2, (480, screen_height // 2 - signuppage.get_height() // 2 + 50))
        screen.blit(signup, (485, screen_height // 2 - signuppage.get_height() // 2 + 100))
        if flag_password == False:
            screen.blit(wrong_password, (600, screen_height // 2 - signuppage.get_height() // 2 + 100))
        else:
            if flag_account == False:
                screen.blit(existed_account, (600, screen_height // 2 - signuppage.get_height() // 2 + 100))
            else:
                if flag_username == False:
                    screen.blit(existed_username, (600, screen_height // 2 - signuppage.get_height() // 2 + 100))

        # Vẽ hình chữ nhật xung quanh vùng nhập dữ liệu
        pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - username.get_height() // 2 - 50 - 10, 170, username.get_height() + 10), 2)
        pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - password_1.get_height() // 2 - 10, 170, password_1.get_height() + 10), 2)
        pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - password_2.get_height() // 2 + 50 - 10, 170, password_2.get_height() + 10), 2)
        pygame.draw.rect(screen, BLACK, (485 - 5, screen_height // 2 - signup.get_height() // 2 + 100 - 10 , 70, signup.get_height() + 10), 2)
      
        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(60)

    # Thoát khỏi Pygame
    #pygame.quit()


def start_all():
    # Định nghĩa màu sắc
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 191, 255)
    RED = (255, 0, 0)

    #return login trả về tên đăng nhập
    tendangnhap = ''

    # Tạo font chữ
    font_1 = pygame.font.Font(None, 36)
    
    # Biến xác định vị trí ô vuông 
    Login_rect = pygame.Rect(550, screen_height // 2 - font_1.get_height() // 2 - 50 - 10 , 190, font_1.get_height() + 20) 
    Signup_rect = pygame.Rect(550, screen_height // 2 - font_1.get_height() // 2 + 50 - 10 , 190, font_1.get_height() + 20) 

    # Hàm kiểm tra xem chuột có nằm trong ô vuông 
    def is_over_Login_box(mouse_pos):
        return Login_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô Reset hay không
    def is_over_Signup_box(mouse_pos):
        return Signup_rect.collidepoint(mouse_pos)

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý sự kiện 
        for event in pygame.event.get():
            if event.type == pygame.QUIT or 8 == 5:
                pygame.quit()  # Thoát khỏi pygame khi nhấn nút tắt màn hình
                quit()  # Thoát khỏi chương trình
            # Bắt sự kiện nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
                if is_over_Login_box(mouse_pos):
                    tendangnhap = login()
                if is_over_Signup_box(mouse_pos):
                    tendangnhap = sign_up()
                return tendangnhap                

        # Tô màu màn hình
        screen.fill(WHITE)
        # # Vẽ hình ảnh Tom and Jerry lên màn hình
        # screen.blit(tom_and_jerry_img, tom_and_jerry_rect)


        # Render và vẽ các thành phần giao diện
        Login = font_1.render("Login", True, BLACK, WHITE)
        Signup = font_1.render("Signup", True, BLUE, WHITE)


        #Vẽ đối tượng văn bản lên màn hình ở vị trí mong muốn
        screen.blit(Login, (screen_width // 2 - Login.get_width() // 2, screen_height // 2 - Login.get_height() // 2 - 50))
        screen.blit(Signup, (screen_width // 2 - Signup.get_width() // 2, screen_height // 2 - Signup.get_height() // 2 + 50))

        # Vẽ hình chữ nhật xung quanh vùng nhập dữ liệu, ô login, ô reset
        pygame.draw.rect(screen, BLACK, (550, screen_height // 2 - Login.get_height() // 2 - 50 - 10 , 190, Login.get_height() + 20), 2)
        pygame.draw.rect(screen, BLACK, (550, screen_height // 2 - Signup.get_height() // 2 + 50 - 10 , 190, Signup.get_height() + 20), 2)
      
        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(60)

    # Thoát khỏi Pygame
    #pygame.quit()

if __name__ == '__main__':
    # pygame setup
    pygame.init()
    #Cửa số game: chỉnh full screen: screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width,screen_height)) 

    # # Load hình ảnh Tom and Jerry
    # tom_and_jerry_img = pygame.image.load('wallpaperflare.com_wallpaper.jpg')  # Đặt đường dẫn tới hình ảnh của bạn ở đây

    # # Vị trí để vẽ hình ảnh Tom and Jerry
    # tom_and_jerry_rect = tom_and_jerry_img.get_rect()
    # tom_and_jerry_rect.center = (screen_width // 2, screen_height // 2)  # Đặt hình ảnh ở giữa màn hình        

    #Đặt tên cho cửa sổ game là Maze
    pygame.display.set_caption('Maze')
    #Hình ảnh tượng trưng cho game đặt bên trái tên cửa sổ game
    # img = pygame.image.load('maze_icon.png')
    # pygame.display.set_icon(img)

    #tạo biến clock truy cập vào đồng hồ trong pygame.time để xử lí về thời gian
    clock = pygame.time.Clock()
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        ss = start_all()
        print(ss)
        break
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
    pygame.quit()

    