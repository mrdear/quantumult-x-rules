const url = $request.url;
if (url.includes("/dpmobile")) {
    const header = $request.headers;
    const resp = {};
    const traceKey = Object.keys(header).find(key => /^m-(shark-)?traceid$/i.test(key));
    const headopt = traceKey ? header[traceKey] : null;

    if (headopt) {
        $done({body: "", headers: "", status: "HTTP/1.1 204 No Content"});
    } else {
        $done({});
    }
} else if (url.includes("/picassovc")) {
    if (!$response.body) $done({});
    let body = $response.body;
    body = body.replace(/function WedgetCard/g, 'function WedgetCard0');
    $done({body});
}