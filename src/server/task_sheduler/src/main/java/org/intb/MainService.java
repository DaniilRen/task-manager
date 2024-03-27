package org.intb;

import org.intb.entity.Blob;
import org.intb.entity.Task;
import org.intb.entity.User;
import org.intb.repositories.BlobRepository;
import org.intb.repositories.TaskRepository;
import org.intb.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

@Service
public class MainService {
    private final UserRepository userRepository;
    private final TaskRepository taskRepository;
    private final BlobRepository blobRepository;

    @Autowired
    public MainService(UserRepository userRepository, TaskRepository taskRepository, BlobRepository blobRepository) {
        this.userRepository = userRepository;
        this.taskRepository = taskRepository;
        this.blobRepository = blobRepository;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public User getUserById(Long id) {
        return userRepository.findById(id).orElse(null);
    }

    public Task getTaskById(Long id) {
        return taskRepository.findById(id).orElse(null);
    }

    public User saveUser(User user) {
        return userRepository.save(user);
    }

    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }

    public void deleteTask(Long id) {
        taskRepository.deleteById(id);
    }

    public User getUserByCredentials(String login, String password) {
        List<User> users = userRepository.findAll().stream().filter(user -> user.isLoginAndPassword(login, password)).toList();
        assert users.size() <= 1;
        if (users.size() == 1) {
            return users.get(0);
        } else {
            return null;
        }
    }
    public List<Task> getTasksForUser(Long userId) {
        return taskRepository.findAll().stream().filter(t -> t.getUserId().equals(userId)).toList();
    }

    public List<Blob> getBlobsForTask(Long taskId) {
        return blobRepository.findAll().stream().filter(t -> t.getTaskID().equals(taskId)).toList();
    }

    public void deleteBlob(Long blobId) {
        blobRepository.deleteById(blobId);
    }

    public Blob saveBlob(Blob blob) {
        return blobRepository.save(blob);
    }

    public Task saveTask(Task task) {
        return taskRepository.save(task);
    }

    public Set<String> getCategories() {
        return new HashSet<>(taskRepository.findAll().stream().map(Task::getTaskClass).toList());
    }

    public boolean isKnownLogin(String login) {
        return userRepository.findAll().stream().map(User::getLogin).toList().contains(login);
    }

    public Optional<User> getUserByLogin(String login) {
        List<User> users = userRepository.findAll().stream().filter(user -> user.getLogin().equals(login)).toList();
        assert users.size() <= 1;
        return users.isEmpty() ? Optional.empty() : Optional.of(users.get(0));
    }
}

