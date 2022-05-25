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
    let $item = (
        `
            <div class="mt-3 container text-center">
                <form method="POST" action="/activity/save" class="form-inline">
                    <ul class="list-group">
                        <H3>${data.activity}</H3>
                        <li class="list-group-item"><b>Participants</b> - ${data.participants}</li>
                        <li class="list-group-item"><b>Price Range</b> - ${data.price}</li>
                        <li class="list-group-item"><b>Type</b> - ${data.type}</li>
                    </ul>
                    <button class="btn btn-success ml-2" type="submit">Save</button>
                    <button class="btn btn-danger ml-2">Ignore</button>
                </form>
            </div>
            `
    );
    $activityDiv.append($item)
    $activityContainer.append($activityDiv)
}