package org.intb.response.task;

import org.intb.response.AbstractResponse;

public class AddTaskResponse extends AbstractResponse {

    private long taskID;

    private long userID;

    public long getTaskID() {
        return taskID;
    }

    public void setTaskID(long taskID) {
        this.taskID = taskID;
    }

    public long getUserID() {
        return userID;
    }

    public void setUserID(long userID) {
        this.userID = userID;
    }
}
