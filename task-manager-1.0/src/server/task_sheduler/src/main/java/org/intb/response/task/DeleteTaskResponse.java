package org.intb.response.task;

import org.intb.response.AbstractResponse;

public class DeleteTaskResponse extends AbstractResponse {
    public long taskID;

    public long getTaskID() {
        return taskID;
    }

    public void setTaskID(long taskID) {
        this.taskID = taskID;
    }
}
