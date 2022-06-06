$(document).ready(function () {
    $('#activityForm').submit(function (evt) {
        evt.preventDefault();
    });
});


async function fetchData() {
    try {
        let $activityContainer = $("#activityContainer");
        $activityContainer.hide()

        let $spinDiv = $("#spinDiv");
        $spinDiv.show();

        const resp = await axios.get("/api/activity");
        const data = resp.data;

        activities = [];
        activities.push(data)

        console.log("INSIDE fetchData", data)

        populateData(data)

        $spinDiv.hide()
        $activityContainer.show()

    } catch (e) {
        console.log(e)
    }
}

function populateData(data) {
    $(".activity-list").remove()
    let $activityContainer = $("#activityContainer");
    const $activityDiv = $("<div>");
    $activityDiv.addClass("activity-list")
    $(".activity-list").empty();
    console.log("INSIDE populateData", data)
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
                <div class="mx-3 container text-center">
                    <ul class="list-group">
                        <H3>${data.activity}</H3>
                        <li class="list-group-item"><b>Participants</b> - ${data.participants}</li>
                        <li class="list-group-item"><b>Price Range</b> - ${data.price}</li>
                        <li class="list-group-item"><b>Type</b> - ${data.type}</li>
                    </ul>
                    <form method="POST" action="/activity/save" class="form-inline">
                        <input type="hidden" name="activityKey" value="${data.key}"/>
                        <input type="hidden" name="activityTitle" value="${data.activity}"/>
                        <input type="hidden" name="activityParticipants" value="${data.participants}"/>
                        <input type="hidden" name="activityPrice" value="${data.price}"/>
                        <input type="hidden" name="activityType" value="${data.type}"/>
                        <button class="btn btn-success ml-2 mt-3" type="submit">Save</button>
                        <button class="btn btn-danger ml-2 mt-3" type="submit">Ignore</button>
                    </form>
                </div>
                `
        );

        $activityDiv.append($item)
        $activityContainer.append($activityDiv)
    }
}



async function getSearchCriteria() {
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

    console.log(participantsVal, priceVal, activityTypeVal)

    axios({
            method: "post",
            url: "/api/activity2",
            data: bodyFormData,
            headers: {
                "Content-Type": "multipart/form-data"
            },
        })
        .then(function (resp) {
            //handle success
            const data = resp.data;

            activities = [];
            activities.push(data)

            console.log("INSIDE fetchData", data)

            populateData(data)

            $spinDiv.hide()
            $activityContainer.show()
        })
        .catch(function (response) {
            //handle error
            console.log(response);
        });
}