package org.intb.response.blob;

import org.intb.response.AbstractResponse;

public class AddBlobResponse extends AbstractResponse {

    private long blobId;

    public long getBlobId() {
        return blobId;
    }

    public void setBlobId(long blobId) {
        this.blobId = blobId;
    }
}
