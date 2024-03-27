package org.intb.response.user;

import org.intb.response.AbstractResponse;

public class AddUserResponse extends AbstractResponse {

    private long userId;

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId1) {
        this.userId = userId1;
    }

}
