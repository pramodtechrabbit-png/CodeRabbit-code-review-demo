package com.demo.service;

import java.util.ArrayList;
import java.util.List;

public class UserService {

    private static List<String> users = new ArrayList<>();

    // 1. No null check
    public void addUser(String username) {
        users.add(username.trim());
    }

    // 2. Exposing internal list
    public List<String> getUsers() {
        return users;
    }

    // 3. Hardcoded password
    public boolean login(String username, String password) {
        if (username.equals("admin") && password.equals("admin123")) {
            return true;
        }
        return false;
    }

    // 4. Poor error handling
    public int divide(int a, int b) {
        try {
            return a / b;
        } catch (Exception e) {
            return 0;
        }
    }

    // 5. Thread safety issue
    public void clearUsers() {
        users.clear();
    }
}
