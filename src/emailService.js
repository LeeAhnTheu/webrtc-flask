// emailService.js
const nodemailer = require('nodemailer');

// Tạo transporter để gửi email
const transporter = nodemailer.createTransport({
    service: 'gmail', // Bạn có thể thay đổi dịch vụ email nếu cần
    auth: {
        user: 'your-email@gmail.com',
        pass: 'your-email-password'
    }
});

// Hàm gửi email
async function sendFallNotification(toEmail, imagePath) {
    const mailOptions = {
        from: 'your-email@gmail.com',
        to: toEmail,
        subject: 'Thông báo té ngã',
        text: 'Hệ thống đã phát hiện một sự cố té ngã. Vui lòng xem hình ảnh đính kèm để biết thêm chi tiết.',
        attachments: [
            {
                filename: 'fall-image.jpg',
                path: imagePath
            }
        ]
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log('Email sent successfully');
    } catch (error) {
        console.error('Error sending email:', error);
    }
}

module.exports = { sendFallNotification };
