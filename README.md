1. Vào file [Try_Space/instance.py] thay đổi n: số lượng đỉnh, N: kích thước quần thể, G: số lượng thế hệ.
2. Thường để N ~ 4*n, G ~ 100 còn lại thì chương trình sẽ dừng nếu 10 thế hệ liên tiếp không update được.
3. Nếu không muốn đọc từ file txt thì chú ý rào lại đoạn code này.
4. Thay vào đó sử dụng ma trận kề thì cần vào file [Try_Space/edAdi_instance.py], thao tác ma trận với ed_graph[] là được.
5. Chạy chương trình với các prompt bị chỉnh sửa thì vào file [Try_Space/config_some_step.py] và run


6. cấu trúc mỗi 1 prompt cho 1 toán tử nào đó: description + pythoncode + example with explanation.
7. Nên sửa các ví dụ với số lượng đỉnh tương ứng ở đồ thị ed_graph. Để sinh ra prompt ví dụ cho một crossover operator thì vào [Try_Space/CrossOver_Operators] là có.
8. viết vào 2 ví dụ cha mẹ rồi run file tương ứng sẽ có prompt ví dụ.

9. CHÚ Ý: không push API key lên github công khai, nếu không sẽ bị google cảnh cáo.
