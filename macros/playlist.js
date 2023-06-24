async function startSong(startTime, listId, songId){
    const plist = game.playlists.get(listId)
    const song = plist.sounds.find(s=> s.id === songId);

    await game.audio.playing.forEach(sound => sound.stop());
    await game.playlists.forEach(playlist => playlist.playing = false);

    await plist.updateEmbeddedDocuments("PlaylistSound", [{_id: song.id, pausedTime: startTime, playing: true}]);
}


async function getSongs(listId){
    const playlist = game.playlists.get(listId);
    const songOptions = playlist.sounds.reduce((acc, song)=> acc += `<option value="${song.id}">${song.name}</option>`,``);
    const songDialogContent = `<form>
                  <div class="form-group">
                        <label>Song:</label>
                        <select name="song-id">${songOptions}</select>
                  </div>
                  <div class="form-group">
                        <label>
                            Start time (in seconds)
                        </label>
                        <input type="number" value="0" name="start-time"/>
                  </div>
            </form>`;

    new Dialog({
        title: "Select song and start time",
        content: songDialogContent,
        buttons: {
            ok: {
                label: "Start",
                callback: (html)=> {
                    let songId = html.find("[name=song-id]")[0].value;
                    let startTime = parseInt(html.find("[name=start-time]")[0].value);
                    startSong(startTime, listId, songId);
                }
            }
        }
    }).render(true);
}

async function getPlaylist() {
    const playlistOptions = game.playlists.reduce((acc,p) => acc += `<option value="${p.id}"> ${p.name}</option>`,``);
    const content = `<form>
                    <div class="form-group">
                        <label>
                            Playlist:
                        </label>
                        
                        <select name="list">${playlistOptions}</select>
                    </div>                    
                 </form>`;

    new Dialog({
        title: "Select Playlist",
        content,
        buttons: {
            ok: {
                label: "Select Playlist",
                callback: (html)=> {
                    const list = html.find("[name=list]")[0].value;

                    getSongs(list);
                }
            }
        }
    }).render(true);
}

await getPlaylist();
