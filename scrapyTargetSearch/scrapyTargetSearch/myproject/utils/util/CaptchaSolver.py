import requests
from PIL import Image, ImageFilter
import pytesseract
import io
import cv2
import numpy as np

# 设置 Tesseract 的路径（如果 Tesseract 没有在环境变量中）
pytesseract.pytesseract.tesseract_cmd = r'E:\tesseract-ocr\tesseract.exe'  # 请根据你的安装路径修改

class CaptchaSolver:
    def __init__(self, captcha_url):
        self.captcha_url = captcha_url
        self.session = requests.Session()

    def get_captcha_image(self):
        """从验证码URL下载验证码图片"""
        try:
            # 获取验证码图片
            response = self.session.get(self.captcha_url)
            response.raise_for_status()  # 检查请求是否成功
            print("验证码图片下载成功")
            return response.content  # 返回图片二进制内容
        except requests.exceptions.RequestException as e:
            print(f"下载验证码失败: {e}")
            return None

    def preprocess_image(self, image):
        """图像预处理，增强OCR识别效果"""
        # 转为灰度图像
        gray_image = image.convert("L")

        # 对图像进行阈值处理，增强对比度
        # 使用 OpenCV 的阈值处理来提高对比度
        cv_image = np.array(gray_image)  # 转换为 NumPy 数组
        _, threshold_image = cv2.threshold(cv_image, 150, 255, cv2.THRESH_BINARY)

        # 转回 Pillow Image 对象
        processed_image = Image.fromarray(threshold_image)

        # 去噪（可选）
        processed_image = processed_image.filter(ImageFilter.MedianFilter(size=3))

        return processed_image

    def solve_captcha(self, captcha_image):
        """识别验证码图片"""
        try:
            # 将二进制验证码数据转为图片对象
            image = Image.open(io.BytesIO(captcha_image))
            
            # 预处理图像
            processed_image = self.preprocess_image(image)

            # 使用 Tesseract OCR 识别图片中的文字
            captcha_text = pytesseract.image_to_string(processed_image, config='--psm 8').strip()  # 使用单个字符识别模式
            print(f"识别的验证码: {captcha_text}")
            return captcha_text
        except Exception as e:
            print(f"识别验证码失败: {e}")
            return None

    def get_and_solve_captcha(self):
        """下载验证码并进行识别"""
        captcha_image = self.get_captcha_image()
        if captcha_image:
            return self.solve_captcha(captcha_image)
        return None

# 示例用法
if __name__ == "__main__":
    captcha_url = 'https://tangsso.cdt-ec.com/iuap-uuas-user/images/getValiImage?ts=1754986435138'  # 实际的验证码URL
    solver = CaptchaSolver(captcha_url)
    
    # 获取验证码并识别
    captcha_text = solver.get_and_solve_captcha()
    if captcha_text:
        print(f"最终验证码: {captcha_text}")
    else:
        print("无法识别验证码")
