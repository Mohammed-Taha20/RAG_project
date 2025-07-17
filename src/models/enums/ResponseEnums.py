from enum import Enum

class Responsesignal(Enum):

    file_type_not_allowed = "File type not allowed"
    file_size_exceeded = "File size exceeded the limit"
    file_uploaded_successfully = "File uploaded successfully"
    file_not_found = "File not found"
    invalid_file_format = "Invalid file format"
    server_error = "Server error occurred"
    unauthorized_access = "Unauthorized access"
    resource_not_found = "Resource not found"
    file_upload_failed = "File upload failed"
    processing_failed = "Processing failed"
    processing_successful = "Processing successful"
    
