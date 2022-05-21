let API_URL = `http://www.boredapi.com/api/`;

async function fetchData() {
    try {
        const resp = await axios.get("http://www.boredapi.com/api/activity");
        const data = resp.data;
        activities = [];
        activities.push(data)
        console.log("INSIDE fetchData", data)
        populateData(data)

    } catch (e) {
        console.log(e)
    }
}

function populateData(data) {
    let $activityContainer = $("#activity");
    const $activityDiv = $("<div>");
    $activityDiv.addClass("activity-list")
    $(".activity-list").empty();
    console.log("INSIDE populateData", data)
    let $item = (
        `
            <div class="mt-3 container text-center"> 
                <ul class="list-group">
                    <H3 id="${data.key}">${data.activity}</H3>
                    <li class="list-group-item"><b>Participants</b> - ${data.participants}</li>
                    <li class="list-group-item"><b>Price Range</b> - ${data.price}</li>
                    <li class="list-group-item"><b>Type</b> - ${data.type}</li>
                </ul>
            </div>
            `
    );
    $activityDiv.append($item)
    $activityContainer.append($activityDiv)


}