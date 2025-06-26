package org.intb.response.blob;

import org.intb.response.AbstractResponse;

public class DeleteBlobResponse extends AbstractResponse {
    private Long blobId;

    public Long getBlobId() {
        return blobId;
    }

    public void setBlobId(Long blobId) {
        this.blobId = blobId;
    }
}
