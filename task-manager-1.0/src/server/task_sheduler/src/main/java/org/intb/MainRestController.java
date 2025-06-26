package org.intb;

import org.intb.entity.Blob;
import org.intb.entity.Task;
import org.intb.entity.User;
import org.intb.requests.*;
import org.intb.requests.blob.AddBlobRequest;
import org.intb.requests.blob.DeleteBlobRequest;
import org.intb.requests.blob.GetBlobsRequest;
import org.intb.requests.task.AddTaskRequest;
import org.intb.requests.task.DeleteTaskRequest;
import org.intb.requests.task.EditTaskRequest;
import org.intb.requests.task.GetTasksRequest;
import org.intb.requests.user.*;
import org.intb.response.*;
import org.intb.response.blob.AddBlobResponse;
import org.intb.response.blob.DeleteBlobResponse;
import org.intb.response.blob.GetBlobsResponse;
import org.intb.response.task.*;
import org.intb.response.user.AddUserResponse;
import org.intb.response.user.DeleteUserResponse;
import org.intb.response.user.EditUserResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api") // Base URL for all REST endpoints
public class MainRestController {

    @Autowired
    private final MainService mainService;

    public MainRestController(MainService mainService) {
        this.mainService = mainService;
    }

    @PostMapping("/add_user")
    public AddUserResponse addUser(@RequestBody AddUserRequest request) {
        if (mainService.isKnownLogin(request.getLogin())) {
            AddUserResponse response = new AddUserResponse();
            response.setSuccess(false);
            return response;
        }
        User user = new User();
        user.setName(request.getName());
        user.setSurname(request.getSurname());
        user.setThirdName(request.getThirdName());
        user.setLogin(request.getLogin());
        user.setPassword(request.getPassword());
        long id = mainService.saveUser(user).getId();
        AddUserResponse response = new AddUserResponse();
        response.setUserId(id);
        return response;
    }

    @PostMapping("/edit_user")
    public EditUserResponse editUser(@RequestBody EditUserRequest request) {
        User userToEdit = mainService.getUserById(request.getId());
        boolean loginWasChanged = !request.getLogin().equals(userToEdit.getLogin());
        Optional<User> userWithNewLogin = mainService.getUserByLogin(request.getLogin());
        if (loginWasChanged && userWithNewLogin.isPresent()) {
            EditUserResponse response = new EditUserResponse();
            response.setSuccess(false);
            return response;
        }
        userToEdit.setName(request.getName());
        userToEdit.setSurname(request.getSurname());
        userToEdit.setThirdName(request.getThirdName());
        userToEdit.setLogin(request.getLogin());
        userToEdit.setPassword(request.getPassword());
        mainService.saveUser(userToEdit);
        EditUserResponse response = new EditUserResponse();
        response.setUserId(userToEdit.getId());
        return response;
    }

    @PostMapping("/delete_user")
    public DeleteUserResponse deleteUser(@RequestBody DeleteUserRequest request) {
        long userID = request.getUserID();
        mainService.deleteUser(userID);
        DeleteUserResponse response = new DeleteUserResponse();
        response.setUserId(userID);
        return response;
    }

    @PostMapping("/list_users")
    public ListUsersResponse listUsers(@RequestBody ListUsersRequest request) {
        List<User> users = mainService.getAllUsers();
        ListUsersResponse response = new ListUsersResponse();
        response.setUsers(users);
        return response;
    }

    @PostMapping("/get_user_by_id")
    public GetUserResponse getUserByID(@RequestBody GetUserByIdRequest request) {
        User user = mainService.getUserById(request.getUserID());
        GetUserResponse response = new GetUserResponse();
        if (user != null) {
            response.setUserId(user.getId());
            response.setSuccess(true);
        } else {
            response.setUserId(0L);
            response.setSuccess(false);
        }
        return response;
    }

    @PostMapping("/get_user_by_credentials")
    public GetUserResponse getUserByCredentials(@RequestBody GetUserByCredentials request) {
        User user = mainService.getUserByCredentials(request.getLogin(), request.getPassword());
        GetUserResponse response = new GetUserResponse();
        if (user != null) {
            response.setUserId(user.getId());
            response.setSuccess(true);
        } else {
            response.setUserId(0L);
            response.setSuccess(false);
        }
        return response;
    }

    @PostMapping("/get_tasks_for_user")
    public GetTasksResponse getTasksForUser(@RequestBody GetTasksRequest request) {
        List<Task> tasks = mainService.getTasksForUser(request.getUserId());
        GetTasksResponse response = new GetTasksResponse();
        response.setTaskList(tasks);
        return response;
    }

    @PostMapping("/add_task")
    public AddTaskResponse addTask(@RequestBody AddTaskRequest request) {
        //System.out.println("Add task for user " + request.getUserId());
        Task task = new Task();
        task.setName(request.getName());
        task.setDescription(request.getDescription());
        task.setTaskClass(request.getTaskClass());
        task.setTaskStatus(request.getTaskStatus());
        task.setUserId(request.getUserId());
        Long taskID = mainService.saveTask(task).getId();
        AddTaskResponse response = new AddTaskResponse();
        response.setTaskID(taskID);
        response.setUserID(request.getUserId());
        return response;
    }

    @PostMapping("/edit_task")
    public EditTaskResponse editTask(@RequestBody EditTaskRequest request) {
        Task task = mainService.getTaskById(request.getTaskId());
        task.setName(request.getName());
        task.setDescription(request.getDescription());
        task.setTaskClass(request.getTaskClass());
        task.setTaskStatus(request.getTaskStatus());
        Long taskID = mainService.saveTask(task).getId();
        EditTaskResponse response = new EditTaskResponse();
        response.setTaskID(taskID);
        return response;
    }

    @PostMapping("/delete_task")
    public DeleteTaskResponse deleteUser(@RequestBody DeleteTaskRequest request) {
        long taskID = request.getTaskID();
        mainService.deleteTask(taskID);
        DeleteTaskResponse response = new DeleteTaskResponse();
        response.setTaskID(taskID);
        return response;
    }

    @PostMapping("/get_categories")
    public GetCategoriesResponse getCategories(@RequestBody GetCategoriesRequest request) {
        GetCategoriesResponse response = new GetCategoriesResponse();
        response.setCategories(mainService.getCategories());
        return response;
    }

    @PostMapping("/add_blob")
    public AddBlobResponse addBlob(@RequestBody AddBlobRequest request) {
        Blob blob = new Blob();
        blob.setBlobData(request.getBlobData());
        blob.setTaskID(request.getTaskId());
        blob.setFileName(request.getFileName());
        long id = mainService.saveBlob(blob).getId();
        AddBlobResponse response = new AddBlobResponse();
        response.setBlobId(id);
        return response;
    }

    @PostMapping("/delete_blob")
    public DeleteBlobResponse deleteBlob(@RequestBody DeleteBlobRequest request) {
        long blobID = request.getBlobId();
        mainService.deleteBlob(blobID);
        DeleteBlobResponse response = new DeleteBlobResponse();
        response.setBlobId(blobID);
        return response;
    }

    @PostMapping("/get_blobs_for_task")
    public GetBlobsResponse getTasksForUser(@RequestBody GetBlobsRequest request) {
        List<Blob> blobs = mainService.getBlobsForTask(request.getTaskId());
        GetBlobsResponse response = new GetBlobsResponse();
        response.setBlobList(blobs);
        return response;
    }
}


