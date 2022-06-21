$(document).ready(function () {
    $('#activityForm').submit(function (evt) {
        evt.preventDefault();
    });
});

async function fetchData() {
    // Get Data from server API and load to HTML
    try {
        let $activityContainer = $("#activityContainer");
        $activityContainer.hide()

        let $spinDiv = $("#spinDiv");
        $spinDiv.show();

        const resp = await axios.get("/api/activity");
        const data = resp.data;

        activities = [];
        activities.push(data)

        populateData(data)

        $spinDiv.hide()
        $activityContainer.show()

    } catch (error) {
        throw(error)
    }
}

function populateData(data) {
    // Load data from API to HTML
    $(".activity-list").remove()
    let $activityContainer = $("#activityContainer");
    const $activityDiv = $("<div>");
    $activityDiv.addClass("activity-list")
    $(".activity-list").empty();
    if (data.activity == undefined) {
        let $noActivityMsg = (
            `
            <div class="mx-3 container text-center">
            <h3> No activity found.Please expand your search and try again.</h3> 
            </div>
            `
        );
        $activityDiv.append($noActivityMsg)
        $activityContainer.append($activityDiv)


    } else {
        let $item = (
            `
                <div class="mx-3 my-3 container text-center">
                    <ul class="list-group">
                        <H3>${data.activity}</H3>
                        <li class="list-group-item border-0"><b><i class="fa fa-users" aria-hidden="true"></i></b> ${data.participants}</li>
                        <li class="list-group-item border-0"><b><i class="fa fa-tags" aria-hidden="true"></i></b> ${data.type}</li>
                    </ul>
                    <form method="POST" class="form-inline">
                        <input type="hidden" name="activityKey" value="${data.key}"/>
                        <input type="hidden" name="activityTitle" value="${data.activity}"/>
                        <input type="hidden" name="activityParticipants" value="${data.participants}"/>
                        <input type="hidden" name="activityPrice" value="${data.price}"/>
                        <input type="hidden" name="activityType" value="${data.type}"/>
                        <button class="btn btn-success ml-2 mt-3 mx-2" type="submit" formaction="/activity/save">Save</button>
                        <button class="btn btn-danger ml-2 mt-3" type="submit" formaction="/activity/ignore">Ignore</button>
                    </form>
                </div>
                `
        );

        $activityDiv.append($item)
        $activityContainer.append($activityDiv)
    }
}

async function getSearchCriteria() {
    // Get values from form and send to server API to receive data back
    let $activityContainer = $("#activityContainer");
    $activityContainer.hide()

    let $spinDiv = $("#spinDiv");
    $spinDiv.show();

    let bodyFormData = new FormData();
    let participantsVal = $("#formParticipants").val()
    bodyFormData.append("participants", participantsVal)

    let priceVal = $("#formPrice").val()
    bodyFormData.append("price", priceVal)

    let activityTypeVal = $("#formActivityType").val()
    bodyFormData.append("activityType", activityTypeVal)

    axios({
            method: "post",
            url: "/api/activity2",
            data: bodyFormData,
            headers: {
                "Content-Type": "multipart/form-data"
            },
        })
        .then(function (resp) {
            const data = resp.data;

            activities = [];
            activities.push(data)

            populateData(data)

            $spinDiv.hide()
            $activityContainer.show()
        })
        .catch(error =>{
            throw(error)
        });
}

function setCompleted(id) {
    // Send checked data to server API to set completed activities
    let activity_Id = document.getElementById(id)
    let checked = document.getElementById(id).checked;
    let bodyFormData = new FormData();
    bodyFormData.append("activity_Id", id)
    bodyFormData.append("isCompleted", checked)
    axios({
            method: "post",
            url: "/api/set_completed",
            data: bodyFormData,
            headers: {
                "Content-Type": "multipart/form-data"
            },
        }).catch(error =>{
            throw(error)
        });
}

function populateNote(id){
    // Populate modal data for saving notes

    let activityNote= document.getElementById("note" + id).innerHTML
    let modalTextArea = document.getElementById("noteArea")
    let activityId = document.getElementById("activityId")
    modalTextArea.value = activityNote
    activityId.value = id
}
