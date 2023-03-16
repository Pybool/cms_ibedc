/**
 * Given a full name, returns an abbreviation consisting of the first letter of each of the first two words in the name that start with a letter or symbol.
 *
 * @param {string} fullname The full name to abbreviate.
 * @returns {string} The abbreviation of the name.
 */
const abbreviateName = ((fullname)=>{
   const charsSymbol = ['#'];
   const charsUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
   const charsLower = 'abcdefghijklmnopqrstuvwxyz'.split('');
   const  p_titles = ['.', 'alj', 'alhaji', 'alhaja', 'mr', 'mrs', 'miss', 'ms', 'dr', '&', 'admiral', 'air', 'comm', 'ambassador', 'baron', 'baroness', 'brig', 'mrs', 'brig', 'gen', 'brigadier', 'brother', 'canon', 'capt', 'chief', 'cllr', 'col', 'commander', 'commander', 'mrs', 'consul', 'consul', 'general', 'count', 'countess', 'countess', 'of', 'cpl', 'dame', 'deputy', 'dr', 'mrs', 'drs', 'duchess', 'duke', 'earl', 'father', 'general', 'gräfin', 'he', 'hma', 'her', 'grace', 'his', 'excellency', 'ing', 'judge', 'justice', 'lady', 'lic', 'llc', 'lord', 'lord', 'lady', 'lt', 'lt', 'col', 'lt', 'cpl', 'm', 'madam', 'madame', 'major', 'major', 'general', 'marchioness', 'marquis', 'minister', 'mme', 'mr', 'dr', 'mr', 'mrs', 'mr', 'ms', 'prince', 'princess', 'professor', 'prof', 'prof', 'dr', 'prof', 'mrs', 'prof', 'rev', 'prof', 'dame', 'prof', 'dr', 'pvt', 'rabbi', 'rear', 'admiral', 'rev', 'rev', 'mrs', 'rev', 'canon', 'rev', 'dr', 'senator', 'sgt', 'sir', 'sir', 'lady', 'sister', 'sqr.', 'leader', 'the', 'earl', 'of', 'the', 'hon', 'the', 'hon', 'dr', 'the', 'hon', 'lady', 'the', 'hon', 'lord', 'the', 'hon', 'mrs', 'the', 'hon', 'sir', 'the', 'honourable', 'the', 'rt', 'hon', 'the', 'rt', 'hon', 'dr', 'the', 'rt', 'hon', 'lord', 'the', 'rt', 'hon', 'sir', 'the', 'rt', 'hon', 'visc', 'viscount']

 
   let abbr = [];
 
   if (fullname.includes('None')) {
     fullname = fullname.replace('None', '');
   } else {
     const splittednames = fullname.split(' ');
     for (const name of splittednames) {
       if (!p_titles.includes(name.toLowerCase())) {
         if (abbr.length < 2) {
           if (charsUpper.includes(name[0]) || charsLower.includes(name[0]) || charsSymbol.includes(name[0])) {
             abbr.push(name);
           }
         } else {
           // Stop looping if we've already found two words to abbreviate.
           break;
         }
       }
     }
   }
 
   switch (abbr.length) {
     case 0:
       return '?';
     case 1:
       return abbr[0][0].toUpperCase();
     case 2:
       return abbr[0][0] + abbr[1][0].toUpperCase();
     default:
       return '';
   }
 })
  

String.prototype.toProperCase = function () {
   return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
 };

// export async function updateAwaitingCustomer(rowid = 0, create = false) {
//    if (!create) {
//      const action = confirm(
//        "Are you sure you want to update this record in the queue? \n\n Updating a record in this manner will not update the account number of this customer"
//      );
//      if (action) {
//        const id = parseInt(rowid);
//        if (hoistedAwaitingCustomer) {
//          const url = `${getBaseUrl()}/cms/update/awaiting_customer/?id=${id}&data=${JSON.stringify(
//            hoistedAwaitingCustomer
//          )}`;
//          const response = await fetch(url);
//          const data = await response.json();
//          if (data.status) {
//            alert(data.message);
//          } else {
//            alert(data.message);
//          }
//        }
//      }
//    } else {
//      if (!rowid) {
//        hoistedAwaitingCustomer.force = "1";
//        const response = await fetch(`${getBaseUrl()}/cms/create_customer_account/`, {
//          method: "POST",
//          body: JSON.stringify(hoistedAwaitingCustomer),
//          headers: {
//            "Content-type": "application/json; charset=UTF-8",
//          },
//        });
//        const { result } = await response.json();
//        const parsedResponse = JSON.parse(result);
//        if (parsedResponse.status && parsedResponse.exists === "False") {
//          alert(parsedResponse.message);
//        } else if (parsedResponse.status && parsedResponse.exists === "True") {
//          const force = confirm(parsedResponse.message);
//        } else {
//          alert(response.message);
//        }
//      }
//    }
//  }

// export function generateExistsDataTemplate(data) {
//    const createLineItem = (item) => {
//      const style = "background:white;color:white;";
//      return `
//        <tr draftid=${item.id} onclick="updateAwaitingCustomer(this.getAttribute('draftid'))" style="${style}" class="nk-tb-item pointer">
//          <td style="${style}" class="nk-tb-col">${item.surname}</td>
//          <td style="${style}" class="nk-tb-col">${item.firstname}</td>
//          <td style="${style}" class="nk-tb-col">${item.othernames}</td>
//          <td style="${style}" class="nk-tb-col">${item.email}</td>
//          <td style="${style}" class="nk-tb-col">${item.mobile}</td>
//          <td style="${style}" class="nk-tb-col">${item.region}</td>
//          <td style="${style}" class="nk-tb-col">${item.buid}</td>
//          <td style="${style}" class="nk-tb-col">${item.servicecenter}</td>
//          <td style="${style}" class="nk-tb-col">${item.create_date}</td>
//          <td style="${style}" class="nk-tb-col">${item.write_date}</td>
//        </tr>
//      `;
//    };
//    const emailLineItemsList = data.email_exists.map((item, index) =>
//      createLineItem(item, index)
//    );
//    const mobileLineItemsList = data.mobile_exists.map((item, index) =>
//      createLineItem(item, index)
//    );
//    const accountNoLineItemsList = data.account_no_exists.map((item, index) =>
//      createLineItem(item, index)
//    );
//    return { emailLineItemsList, mobileLineItemsList, accountNoLineItemsList };
//  }


 
 
 


exports.abbreviateName = abbreviateName