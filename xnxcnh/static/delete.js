// xnx-cnh (c) by Vladislav 'ElCapitan' Nazarov
// 
// xnx-cnh is licensed under a
// Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
// 
// You should have received a copy of the license along with this
// work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

function DeleteI(id, url, add = "nd", uid = "nd") {
    if (!confirm('Confirm deletion')) {
        return
    }

    $.ajax({
        type     : "POST",
        url      : url,
        datatype : "json",
        data : {
            "id"   : id,
            "uid"  : uid,
            DELETE : `${add}`
        }
    })

    setTimeout(() => {
        document.location.reload();
      }, 10);   
}