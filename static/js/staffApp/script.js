//custom issue list
let issueDetails = {
  issueId: "ISSUE-2023-11-8593",
  issueType: "Others",
  project: "iBAS++",
  status: "Submitted",
  userName: "Mohammad Wakib Hasan",
  userMobile: "01576538723",
  emailId: "user.email@gmail.com",
  createdBy: "Chatbot",
  createdOn: "12.20 PM, 24 Dec, 2023",
  description: "This is the description of issue",
};
const issueId = document.getElementById("issueId");
const issueType = document.getElementById("issueType");
const project = document.getElementById("project");
const status = document.getElementById("status");
const userName = document.getElementById("userName");
const userMobile = document.getElementById("userMobileNo");
const emailId = document.getElementById("emailId");
const createdBy = document.getElementById("createdBy");
const createdOn = document.getElementById("createdOn");
const description = document.getElementById("description");
issueId.innerHTML = issueDetails.issueId;
issueType.innerHTML = issueDetails.issueType;
project.innerHTML = issueDetails.project;
status.innerHTML = issueDetails.status;
userName.innerHTML = issueDetails.userName;
userMobile.innerHTML = issueDetails.userMobile;
emailId.innerHTML = issueDetails.emailId;
createdBy.innerHTML = issueDetails.createdBy;
createdOn.innerHTML = issueDetails.createdOn;
description.innerHTML = issueDetails.description;
