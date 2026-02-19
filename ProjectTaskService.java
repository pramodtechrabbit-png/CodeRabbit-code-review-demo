package com.demo.service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ProjectTaskService {

    private final List<String> projects = Collections.synchronizedList(new ArrayList<>());
    private final List<String> tasks = Collections.synchronizedList(new ArrayList<>());
    private final List<String> users = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded admin key (reviewable)
    private static final String ADMIN_KEY = "PROJECT-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(3);

    // Add project with validation
    public boolean addProject(String projectId) {
        if (projectId == null || projectId.trim().isEmpty()) {
            System.out.println("Invalid projectId"); // Reviewable
            return false;
        }
        synchronized (projects) {
            if (projects.contains(projectId.trim())) {
                System.out.println("Duplicate project"); // Reviewable
                return false;
            }
            projects.add(projectId.trim());
        }
        return true;
    }

    // Add user with validation
    public boolean addUser(String userId) {
        if (userId == null || userId.trim().isEmpty()) {
            System.out.println("Invalid userId"); // Reviewable
            return false;
        }
        synchronized (users) {
            if (users.contains(userId.trim())) {
                System.out.println("Duplicate user"); // Reviewable
                return false;
            }
            users.add(userId.trim());
        }
        return true;
    }

    // Add task with validation
    public boolean addTask(String taskId, String projectId, String userId) {
        if (taskId == null || taskId.trim().isEmpty()) {
            System.out.println("Invalid taskId"); // Reviewable
            return false;
        }
        if (!projects.contains(projectId)) {
            System.out.println("Project does not exist"); // Reviewable
            return false;
        }
        if (!users.contains(userId)) {
            System.out.println("User does not exist"); // Reviewable
            return false;
        }
        synchronized (tasks) {
            tasks.add(taskId.trim());
        }
        return true;
    }

    // Async task assignment
    public void submitAsyncTask(String taskId, String projectId, String userId) {
        executor.submit(() -> {
            try {
                addTask(taskId, projectId, userId);
                System.out.println("Async task submitted: " + taskId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Admin authentication
    public boolean authenticateAdmin(String key) {
        if (key == null || key.isEmpty()) return false;
        return ADMIN_KEY.equals(key); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getProjects() {
        synchronized (projects) { return new ArrayList<>(projects); }
    }

    public List<String> getTasks() {
        synchronized (tasks) { return new ArrayList<>(tasks); }
    }

    public List<String> getUsers() {
        synchronized (users) { return new ArrayList<>(users); }
    }

    // Clear all data
    public void clearAll() {
        synchronized (projects) { projects.clear(); }
        synchronized (tasks) { tasks.clear(); }
        synchronized (users) { users.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
