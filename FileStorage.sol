// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileStorage {
    struct File {
        string fileType;
        string fileHash;
    }

    mapping(uint256 => File) public files;
    uint256 public fileCount;

    event FileUploaded(uint256 fileId, string fileType, string fileHash);

    function uploadFile(string memory _fileType, string memory _fileHash) public {
        fileCount++;
        files[fileCount] = File(_fileType, _fileHash);
        emit FileUploaded(fileCount, _fileType, _fileHash);
    }
}
