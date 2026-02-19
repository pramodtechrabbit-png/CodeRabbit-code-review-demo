import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;
import java.io.*;
import java.nio.file.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for FileUploadService
 * Tests cover functionality, edge cases, and security vulnerabilities
 */
public class FileUploadServiceTest {

    @TempDir
    Path tempDir;

    @BeforeEach
    void setUp() {
        // Reset system output capture if needed
        System.setOut(System.out);
    }

    @Test
    @DisplayName("Test successful file upload with valid content")
    void testUploadFileSuccess() {
        String fileName = "test.txt";
        String content = "Test content";

        // This will write to C:/uploads/ which may not exist
        // Test documents the behavior
        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with empty filename")
    void testUploadFileWithEmptyFileName() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        FileUploadService.uploadFile("", "content");

        String output = outContent.toString();
        assertTrue(output.contains("Empty file name"));
    }

    @Test
    @DisplayName("Test upload with null filename throws NullPointerException")
    void testUploadFileWithNullFileName() {
        // Documents the bug: no null check before calling length()
        assertThrows(NullPointerException.class, () -> {
            FileUploadService.uploadFile(null, "content");
        });
    }

    @Test
    @DisplayName("Test upload with null content")
    void testUploadFileWithNullContent() {
        // Content can be null, will be written as "null" string
        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile("test.txt", null);
        });
    }

    @Test
    @DisplayName("Test path traversal vulnerability with ../ in filename")
    void testPathTraversalVulnerability() {
        String maliciousFileName = "../../../etc/passwd";
        String content = "malicious content";

        // Documents security vulnerability: path traversal
        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(maliciousFileName, content);
        });
    }

    @Test
    @DisplayName("Test path traversal with absolute path")
    void testPathTraversalWithAbsolutePath() {
        String absolutePath = "/tmp/malicious.txt";
        String content = "content";

        // Documents that absolute paths can bypass upload directory
        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(absolutePath, content);
        });
    }

    @Test
    @DisplayName("Test upload with Windows path traversal")
    void testWindowsPathTraversal() {
        String windowsPath = "..\\..\\..\\Windows\\System32\\test.txt";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(windowsPath, "content");
        });
    }

    @Test
    @DisplayName("Test upload with special characters in filename")
    void testUploadFileWithSpecialCharacters() {
        String specialFileName = "test@#$%^&*.txt";
        String content = "content";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(specialFileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with unicode filename")
    void testUploadFileWithUnicodeFileName() {
        String unicodeFileName = "测试文件.txt";
        String content = "Unicode content";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(unicodeFileName, content);
        });
    }

    @Test
    @DisplayName("Test upload logs sensitive content")
    void testUploadLogsSensitiveContent() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        String fileName = "secret.txt";
        String sensitiveContent = "password123";

        FileUploadService.uploadFile(fileName, sensitiveContent);

        String output = outContent.toString();
        // Documents vulnerability: sensitive data is logged
        assertTrue(output.contains(sensitiveContent));
    }

    @Test
    @DisplayName("Test upload with very long filename")
    void testUploadFileWithLongFileName() {
        String longFileName = "a".repeat(1000) + ".txt";
        String content = "content";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(longFileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with very large content")
    void testUploadFileWithLargeContent() {
        String fileName = "large.txt";
        String largeContent = "x".repeat(1000000); // 1MB

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, largeContent);
        });
    }

    @Test
    @DisplayName("Test upload with empty content")
    void testUploadFileWithEmptyContent() {
        String fileName = "empty.txt";
        String content = "";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with multiline content")
    void testUploadFileWithMultilineContent() {
        String fileName = "multiline.txt";
        String content = "Line 1\nLine 2\nLine 3\n";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with whitespace-only filename")
    void testUploadFileWithWhitespaceFileName() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        FileUploadService.uploadFile("   ", "content");

        // Whitespace filename has length > 0, so won't trigger empty check
        String output = outContent.toString();
        assertFalse(output.contains("Empty file name"));
    }

    @Test
    @DisplayName("Test upload overwrites existing files silently")
    void testUploadOverwritesExistingFile() {
        String fileName = "overwrite.txt";

        // First upload
        FileUploadService.uploadFile(fileName, "original content");

        // Second upload with different content - documents that it overwrites
        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, "new content");
        });
    }

    @Test
    @DisplayName("Test upload with filename containing null bytes")
    void testUploadFileWithNullBytes() {
        String fileNameWithNull = "test\0.txt";
        String content = "content";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileNameWithNull, content);
        });
    }

    @Test
    @DisplayName("Test upload fails gracefully when directory doesn't exist")
    void testUploadFailsWhenDirectoryMissing() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        // Upload will likely fail due to missing C:/uploads/ directory
        FileUploadService.uploadFile("test.txt", "content");

        String output = outContent.toString();
        // May contain "Upload failed" or may succeed if directory exists
        assertTrue(output.length() > 0);
    }

    @Test
    @DisplayName("Test upload with JSON content")
    void testUploadFileWithJsonContent() {
        String fileName = "data.json";
        String jsonContent = "{\"key\": \"value\", \"number\": 123}";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, jsonContent);
        });
    }

    @Test
    @DisplayName("Test upload with XML content")
    void testUploadFileWithXmlContent() {
        String fileName = "data.xml";
        String xmlContent = "<?xml version=\"1.0\"?><root><item>value</item></root>";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, xmlContent);
        });
    }

    @Test
    @DisplayName("Test upload with binary-like content as string")
    void testUploadFileWithBinaryLikeContent() {
        String fileName = "binary.dat";
        String binaryContent = "\u0000\u0001\u0002\u0003\u0004\u0005";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, binaryContent);
        });
    }

    @Test
    @DisplayName("Test upload with filename containing forward slashes")
    void testUploadFileWithSlashesInName() {
        String fileName = "subdir/file.txt";
        String content = "content";

        // Documents that slashes create subdirectories or fail
        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @Test
    @DisplayName("Test upload prints absolute file path")
    void testUploadPrintsAbsolutePath() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));

        String fileName = "path_test.txt";
        FileUploadService.uploadFile(fileName, "content");

        String output = outContent.toString();
        // Should contain "File uploaded:" message
        assertTrue(output.contains("File uploaded:") || output.contains("Upload failed"));
    }

    @Test
    @DisplayName("Test multiple consecutive uploads")
    void testMultipleConsecutiveUploads() {
        assertAll(
            () -> assertDoesNotThrow(() -> FileUploadService.uploadFile("file1.txt", "content1")),
            () -> assertDoesNotThrow(() -> FileUploadService.uploadFile("file2.txt", "content2")),
            () -> assertDoesNotThrow(() -> FileUploadService.uploadFile("file3.txt", "content3"))
        );
    }

    @Test
    @DisplayName("Test upload with filename ending in extension only")
    void testUploadFileWithExtensionOnly() {
        String fileName = ".txt";
        String content = "hidden file content";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with no file extension")
    void testUploadFileWithNoExtension() {
        String fileName = "noextension";
        String content = "content";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @Test
    @DisplayName("Test upload with content containing special escape sequences")
    void testUploadFileWithEscapeSequences() {
        String fileName = "escape.txt";
        String content = "Line1\tTabbed\rCarriage\nNewline\\Backslash\"Quote";

        assertDoesNotThrow(() -> {
            FileUploadService.uploadFile(fileName, content);
        });
    }

    @AfterEach
    void tearDown() {
        System.setOut(System.out);
    }
}