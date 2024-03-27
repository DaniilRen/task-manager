package org.intb.response.blob;

import org.intb.entity.Blob;
import org.intb.response.AbstractResponse;

import java.util.List;

public class GetBlobsResponse extends AbstractResponse {
    private List<Blob> blobList;

    public List<Blob> getBlobList() {
        return blobList;
    }

    public void setBlobList(List<Blob> blobList) {
        this.blobList = blobList;
    }
}
