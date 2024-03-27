package org.intb.response.user;

import org.intb.response.AbstractResponse;

public class DeleteUserResponse extends AbstractResponse {

    private long userId;

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }
}
