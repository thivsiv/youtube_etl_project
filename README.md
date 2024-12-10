
# YouTube ETL Pipeline

A robust ETL (Extract, Transform, Load) pipeline that fetches video metadata from a specified YouTube channel, transforms the data, and uploads it as a CSV file to an AWS S3 bucket. Additionally, the project files can be seamlessly uploaded and run on an AWS EC2 instance.

## 🚀 Features

- Extracts video metadata (title, description, and URL) from a YouTube channel using the YouTube Data API.
- Cleans and transforms the video descriptions for better readability.
- Saves the processed data to a timestamped CSV file.
- Uploads the CSV file to an AWS S3 bucket for centralized storage.
- Allows the project to be deployed and executed directly on an AWS EC2 instance.

## 🛠️ Technologies Used

- **Python**: Core language for scripting and data processing.
- **YouTube Data API v3**: For fetching video metadata.
- **AWS S3**: For cloud-based storage of the extracted data.
- **AWS EC2**: To host and run the ETL pipeline.
- **pandas**: For data manipulation and CSV generation.
- **dotenv**: For managing sensitive credentials via environment variables.
- **boto3**: AWS SDK for Python to interact with S3.

## 📂 Project Structure

```plaintext
├── youtube_etl.py    # Main script for the ETL process
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (API keys and credentials)
├── README.md         # Project documentation
```

## ⚙️ Setup and Installation

### **On Local Machine**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/thivsiv/youtube_etl_project.git
   cd youtube_etl
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root and add the following:
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key
   AWS_ACCESS_KEY=your_aws_access_key
   AWS_SECRET_KEY=your_aws_secret_key
   BUCKET_NAME=your_s3_bucket_name
   ```

5. **Test the script locally**:
   Replace `channel_id` in `youtube_etl.py` with the desired YouTube channel ID and run:
   ```bash
   python youtube_etl.py
   ```

### **On AWS EC2 Instance**
1. **Launch an EC2 instance**:
   - Choose an Amazon Linux or Ubuntu AMI.
   - Configure the instance with sufficient storage and security group settings.

2. **Connect to your EC2 instance**:
   ```bash
   ssh -i your_key.pem ec2-user@your-ec2-public-ip 

3. **Transfer files to EC2**:
   Use `scp` to upload all files to your EC2 instance:
   ```bash
   scp -i your_key.pem -r /path/to/your/local/project ec2-user@your-ec2-public-ip:/home/ec2-user/
   ```

4. **Set up the EC2 environment**:
   ```bash
   sudo yum update -y
   sudo yum install python3 -y
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run the ETL script on EC2**:
   ```bash
   python youtube_etl.py
   ```

## 🔄 Usage

1. **Fetch and transform YouTube video data**:
   Replace `channel_id` in the script with the desired YouTube channel ID.

2. **Output**:
   - A CSV file with video data will be generated and saved locally.
   - The file will also be uploaded to the specified AWS S3 bucket.

3. **Deploy and run on EC2**:
   Easily execute the ETL process from the cloud using your EC2 instance.

## 📝 Notes

- Ensure that the YouTube API key has permissions to access the YouTube Data API.
- AWS credentials should have appropriate permissions to upload files to the specified S3 bucket.
- The ETL process assumes that every video item contains a `videoId`. If not, the script will log the error.

## 🔧 Troubleshooting

- **`ModuleNotFoundError: No module named 'dotenv'`**  
  Ensure you’ve installed all dependencies using the command:
  ```bash
  pip install -r requirements.txt
  ```

- **`KeyError: 'videoId'`**  
  This error occurs if a result item from the YouTube API response lacks a `videoId`. Modify the script to handle such cases gracefully.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgements

- [Google YouTube Data API](https://developers.google.com/youtube/registering_an_application)
- [AWS S3 Documentation](https://aws.amazon.com/s3/)
- [AWS EC2 Documentation](https://aws.amazon.com/ec2/)

---

