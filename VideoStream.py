import re
import struct
import os


class VideoStream:
	def __init__(self, filename):
		self.filename = filename
		try:
			# Mở file ở chế độ nhị phân (rb)
			self.file = open(filename, 'rb')
		except:
			raise IOError
		self.frameNum = 0
		# Byte đánh dấu cuối khung hình JPEG (End of Image - EOI)
		self.EOI = b'\xFF\xD9'

	def nextFrame(self):
		"""Get next frame by searching for the JPEG End of Image (EOI) marker."""
        
        # --- LOGIC DÀNH CHO TỆP MJPEG THÔ (RAW MJPEG) ---
        # Đọc dữ liệu từ vị trí hiện tại
		data = self.file.read(os.path.getsize(self.filename) - self.file.tell())
        
		if not data:
			return None # Hết tệp
            
        # Tìm vị trí của điểm kết thúc khung hình JPEG (0xFF D9)
        # Bắt đầu tìm kiếm ngay từ đầu dữ liệu đã đọc
		eoi_pos = data.find(self.EOI)
        
		if eoi_pos == -1:
            # Nếu không tìm thấy EOI, có thể là khung hình cuối cùng bị cắt
            # Hoặc tệp bị lỗi. Trả về None nếu không có thêm dữ liệu.
			if len(data) > 0:
				print("Warning: EOI marker not found in the last chunk of data.")
			return None
        
        # Vị trí của byte D9 là eoi_pos + 1. 
        # Khung hình hoàn chỉnh bao gồm cả 0xFF D9, nên lấy eoi_pos + 2
		frame_end_index = eoi_pos + 2 
        
        # Dữ liệu khung hình là từ đầu cho đến EOI (bao gồm EOI)
		frame_data = data[:frame_end_index]
        
        # Cập nhật con trỏ file: di chuyển đến ngay sau EOI để sẵn sàng đọc khung hình tiếp theo
		self.file.seek(self.file.tell() - len(data) + frame_end_index)
        
        # --- KIỂM TRA CHO CÁC TỆP CÓ HEADER KÍCH THƯỚC (Disabled vì gây lỗi) ---
        # Nếu muốn hỗ trợ cả hai, bạn cần một cơ chế phát hiện tốt hơn.
        # Ví dụ, nếu frame_data bắt đầu bằng b'\xFF\xD8' (SOI), thì đây là MJPEG thô.
        
		self.frameNum += 1
		return frame_data
	
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum