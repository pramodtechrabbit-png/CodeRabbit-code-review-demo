import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class FileUploadService {

    private static String uploadDir = "C:/uploads/";  // Hardcoded path

    public static void uploadFile(String fileName, String content) {

        try {

            // No null check
            if (fileName.length() == 0) {
                System.out.println("Empty file name");
            }

            // Path traversal vulnerability
            File file = new File(uploadDir + fileName);

            // Overwrites existing files silently
            FileWriter writer = new FileWriter(file);

            writer.write(content);

            // Sensitive data logging
            System.out.println("File uploaded: " + file.getAbsolutePath());
            System.out.println("Content: " + content);

            writer.close();

        } catch (IOException e) {

            // Ignoring proper logging
            System.out.println("Upload failed");

        }
    }
}
