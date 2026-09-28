
"""Mã sinh viên: 202419071
Họ tên: Vũ Bảo Khôi"""


class Employee:
    """Lớp đại diện cho nhân sự thông thường."""
    def __init__(self, id="UNKNOWN", fullName="Unnamed employee", baseSalary=0.0):
        if not id or not fullName:
            raise ValueError("Mã nhân sự và họ tên không được rỗng.")
        if baseSalary < 0:
            raise ValueError("Lương cơ bản không được âm.")
        self._id = id
        self._fullName = fullName
        self._baseSalary = baseSalary

    @property
    def id(self):
        return self._id

    @property
    def full_name(self):
        return self._fullName

    @property
    def base_salary(self):
        return self._baseSalary

    def increase_salary(self, value, by_percentage=False):
        if value <= 0:
            raise ValueError("Giá trị tăng phải là số dương.")
        if by_percentage:
            self._baseSalary += self._baseSalary * (value / 100.0)
        else:
            self._baseSalary += value

    def calculate_monthly_cost(self):
        return self._baseSalary

    def display_info(self):
        print(f"[Employee] Mã: {self._id} | Họ tên: {self._fullName} | Lương cơ bản: {self._baseSalary:,.2f}")

    def __del__(self):
        print(f"-> [Vòng đời] Đối tượng Employee '{self._id} - {self._fullName}' đã được thu hồi.")


class SoftwareEngineer(Employee):
    """Lớp kỹ sư phần mềm kế thừa từ Employee."""
    def __init__(self, id="UNKNOWN", fullName="Unnamed employee", baseSalary=0.0, primaryLanguage="Python", technicalAllowance=0.0):
        super().__init__(id, fullName, baseSalary)
        if not primaryLanguage:
            raise ValueError("Ngôn ngữ lập trình chính không được rỗng.")
        if technicalAllowance < 0:
            raise ValueError("Phụ cấp kỹ thuật không được âm.")
        self._primaryLanguage = primaryLanguage
        self._technicalAllowance = technicalAllowance

    @property
    def primary_language(self):
        return self._primaryLanguage

    @property
    def technical_allowance(self):
        return self._technicalAllowance

    def calculate_monthly_cost(self):
        return self.base_salary + self._technicalAllowance

    def display_info(self):
        print(f"[SoftwareEngineer] Mã: {self.id} | Họ tên: {self.full_name} | Ngôn ngữ: {self._primaryLanguage} | Lương cơ bản: {self.base_salary:,.2f} | Phụ cấp: {self._technicalAllowance:,.2f} | Tổng chi phí: {self.calculate_monthly_cost():,.2f}")

    def __del__(self):
        print(f"-> [Vòng đời] Đối tượng SoftwareEngineer '{self.id} - {self.full_name}' đã được thu hồi.")


class ProjectTeam:
    """Lớp quản lý nhóm dự án (liên kết không sở hữu đến nhân sự)."""
    def __init__(self, projectCode, projectName, leader=None):
        if not projectCode or not projectName:
            raise ValueError("Mã dự án và tên dự án không được rỗng.")
        self._projectCode = projectCode
        self._projectName = projectName
        self._leader = None
        self._members = []
        
        if leader is not None:
            self.add_member(leader, make_leader=True)

    @property
    def project_code(self):
        return self._projectCode

    @property
    def project_name(self):
        return self._projectName

    @property
    def leader(self):
        return self._leader

    @property
    def members(self):
        return self._members

    def contains(self, employee_id):
        return any(m.id == employee_id for m in self._members)

    def add_member(self, employee, make_leader=False):
        if self.contains(employee.id):
            if make_leader:
                self._leader = employee
            return False
        
        self._members.append(employee)
        if make_leader:
            self._leader = employee
        return True

    def remove_member(self, employee_id):
        if self._leader and self._leader.id == employee_id:
            raise ValueError("Thao tác bị từ chối: Không được xóa trưởng nhóm khi chưa chọn trưởng nhóm thay thế.")
        
        for i, m in enumerate(self._members):
            if m.id == employee_id:
                del self._members[i]
                return True
        return False

    def change_leader(self, employee):
        if not self.contains(employee.id):
            self.add_member(employee, make_leader=False)
        self._leader = employee

    def calculate_total_monthly_cost(self):
        return sum(m.calculate_monthly_cost() for m in self._members)

    def display_team(self):
        print(f"\n============================================================")
        print(f"NHÓM DỰ ÁN: [{self._projectCode}] {self._projectName}")
        leader_info = f"{self._leader.full_name} (ID: {self._leader.id})" if self._leader else "Chưa phân công"
        print(f"Trưởng nhóm: {leader_info}")
        print(f"Danh sách thành viên ({len(self._members)}):")
        for m in self._members:
            role_tag = " [TRƯỞNG NHÓM]" if self._leader and self._leader.id == m.id else ""
            print(f"  - ({m.id}) {m.full_name} | Chi phí tháng: {m.calculate_monthly_cost():,.2f}{role_tag}")
        print(f"Tổng chi phí nhân sự hằng tháng: {self.calculate_total_monthly_cost():,.2f}")
        print(f"============================================================")

    def __del__(self):
        print(f"-> [Vòng đời] ProjectTeam '{self._projectCode}' hủy cấu trúc danh sách liên kết nội bộ. Các đối tượng nhân sự độc lập được bảo toàn.")


# ==========================================
# CHƯƠNG TRÌNH KIỂM THỬ
# ==========================================
if __name__ == "__main__":
    print("=== BẮT ĐẦU CHƯƠNG TRÌNH KIỂM THỬ ==-\n")

    # 1. Tạo hai Employee bằng hai constructor khác nhau
    print("--- 1. Tạo các nhân sự thông thường ---")
    emp1 = Employee("EMP01", "Nguyen Van An", 10000000)
    emp2 = Employee("EMP02", "Tran Thi Binh") # Dùng constructor mặc định baseSalary = 0
    emp1.display_info()
    emp2.display_info()

    # 2. Tạo hai SoftwareEngineer bằng hai constructor khác nhau
    print("\n--- 2. Tạo các kỹ sư phần mềm ---")
    se1 = SoftwareEngineer("SE01", "Le Hoang Nam", 15000000, "Python", 3000000)
    se2 = SoftwareEngineer("SE02", "Pham Minh Chau", 18000000, "TypeScript", 4000000)
    se1.display_info()
    se2.display_info()

    # 3. Tăng lương một nhân sự bằng số tiền cố định
    print("\n--- 3. Tăng lương cố định cho EMP02 ---")
    emp2.increase_salary(5000000, by_percentage=False)
    emp2.display_info()

    # 4. Tăng lương một nhân sự khác theo phần trăm
    print("\n--- 4. Tăng lương theo % cho SE1 ---")
    se1.increase_salary(10.0, by_percentage=True) # Tăng 10%
    se1.display_info()

    # 5. Tạo nhóm dự án không có trưởng nhóm
    print("\n--- 5. Tạo nhóm dự án chưa có trưởng nhóm ---")
    team1 = ProjectTeam("PROJ01", "He Thong Quan Ly Nhan Su")
    team1.display_team()

    # 6. Thêm một nhân sự vào nhóm bằng addMember(employee)
    print("\n--- 6. Thêm EMP01 vào nhóm 1 ---")
    team1.add_member(emp1)
    team1.display_team()

    # 7. Thêm một kỹ sư bằng addMember(employee, true) để đặt làm trưởng nhóm
    print("\n--- 7. Thêm SE1 làm trưởng nhóm dự án 1 ---")
    team1.add_member(se1, make_leader=True)
    team1.display_team()

    # 8. Thử thêm lại một thành viên đã tồn tại
    print("\n--- 8. Thử thêm lại EMP01 đã có trong nhóm ---")
    added_again = team1.add_member(emp1)
    print(f"Kết quả thêm lại EMP01: {added_again}")

    # 9. Hiển thị danh sách bằng lời gọi đa hình
    print("\n--- 9. Hiển thị thông tin qua đa hình (Polymorphism) ---")
    for member in team1.members:
        member.display_info() # Gọi phương thức ghi đè tương ứng (Employee hoặc SoftwareEngineer)

    # 10. Tính tổng chi phí nhân sự hằng tháng
    print(f"\n--- 10. Tổng chi phí hằng tháng của nhóm 1: {team1.calculate_total_monthly_cost():,.2f} ---")

    # 11. Thử xóa trưởng nhóm hiện tại và kiểm tra thao tác bị từ chối
    print("\n--- 11. Thử xóa trưởng nhóm hiện tại (SE01) ---")
    try:
        team1.remove_member(se1.id)
    except ValueError as e:
        print(f"Bắt ngoại lệ thành công: {e}")

    # 12. Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm
    print("\n--- 12. Đổi trưởng nhóm sang EMP01 và xóa SE01 cũ ---")
    team1.change_leader(emp1)
    team1.remove_member(se1.id) # Bây giờ có thể xóa vì SE01 không còn là trưởng nhóm
    team1.display_team()

    # 13. Tạo nhóm thứ hai và thêm nhân sự đã có ở nhóm 1 (chứng minh quan hệ kết tập nhiều nhóm)
    print("\n--- 13. Tạo nhóm 2 và chia sẻ nhân sự emp2 từ nhóm 1 ---")
    team1.add_member(emp2) # Thêm emp2 vào nhóm 1 trước
    team2 = ProjectTeam("PROJ02", "AI Face Recognition Attendance", leader=emp2)
    team2.add_member(emp1) # emp1 tham gia đồng thời cả 2 nhóm
    team2.display_team()

    # 14. Hủy nhóm thứ hai bằng cách kết thúc khối lệnh cục bộ / hủy tường minh
    print("\n--- 14. Hủy nhóm thứ hai ---")
    del team2

    # 15. Chứng minh nhân sự của nhóm thứ hai vẫn tồn tại sau khi nhóm bị hủy
    print("\n--- 15. Kiểm tra nhân sự EMP02 vẫn tồn tại độc lập sau khi nhóm 2 bị hủy ---")
    emp2.display_info()
    print("=== KẾT THÚC KIỂM THỬ ===")