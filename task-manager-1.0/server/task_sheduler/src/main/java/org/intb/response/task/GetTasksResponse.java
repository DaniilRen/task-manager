package org.intb.response.task;

import org.intb.entity.Task;
import org.intb.response.AbstractResponse;

import java.util.List;

public class GetTasksResponse extends AbstractResponse {

    private List<Task> taskList;

    public List<Task> getTaskList() {
        return taskList;
    }

    public void setTaskList(List<Task> taskList) {
        this.taskList = taskList;
    }
}
