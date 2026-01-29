export default function (component) {
    const { parentElement, data } = component;

    const tableHead = parentElement.querySelector("#tableHead");
    const tableBody = parentElement.querySelector("#tableBody");
    const displayYear = parentElement.querySelector("#displayYear");

    const monthNamesShort = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

    let currentYear = new Date().getFullYear();

    function renderTable(year) {
        const today = new Date();
        const realCurrentMonth = today.getMonth(); // 0-11
        const realCurrentYear = today.getFullYear();

        let headerHTML = `<tr><th class="col-fixed">Obras</th>`;

        for (let m = 0; m < 12; m++) {
            const isCurrentMonth = (year === realCurrentYear && m === realCurrentMonth);
            const classToday = isCurrentMonth ? "is-today-col" : "";

            headerHTML += `
                <th class="col-month ${classToday}">
                    <div class="th-content">
                        <span class="th-month-name">${monthNamesShort[m]}</span>
                    </div>
                </th>`;
        }
        headerHTML += `</tr>`;
        tableHead.innerHTML = headerHTML;
        tableBody.innerHTML = "";

        const dadosDoAno = data.filter(item => {
            const d = new Date(item.data_relatorio);
            return d.getFullYear() === year;
        });

        const projetosUnicos = [...new Set(data.map(item => item.sigla))].sort();

        projetosUnicos.forEach(projeto => {
            const row = document.createElement("tr");

            const cellName = document.createElement("td");
            cellName.classList.add("col-fixed");
            cellName.textContent = projeto;
            row.appendChild(cellName);

            const dadosObra = dadosDoAno.filter(item => item.sigla === projeto);

            for (let m = 0; m < 12; m++) {
                const isToday = year === realCurrentYear && m === realCurrentMonth;
                const cell = document.createElement("td");
                cell.className = "col-month" + (isToday ? " is-today-col" : "");

                const isFuture = year > realCurrentYear || (year === realCurrentYear && m > realCurrentMonth);
                const temRegistro = dadosObra.some(item => {
                    const d = new Date(item.data_relatorio);
                    return d.getFullYear() === year && d.getMonth() === m;
                });

                if (temRegistro || !isFuture) {
                    const status = temRegistro ? 'check' : 'x';
                    const svgIcon = status === 'check'
                        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
                        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';

                    const iconDiv = document.createElement("div");
                    iconDiv.className = `icon-box ${status}`;
                    iconDiv.innerHTML = svgIcon;
                    cell.appendChild(iconDiv);
                }

                row.appendChild(cell);
            }
            tableBody.appendChild(row);
        });
        displayYear.textContent = year;
        parentElement.querySelector("#nextBtn").disabled = year >= new Date().getFullYear();
    }

    function changeYear(offset) {
        currentYear += offset;
        renderTable(currentYear);
    }

    parentElement.querySelector("#prevBtn").addEventListener("click", () => changeYear(-1));
    parentElement.querySelector("#nextBtn").addEventListener("click", () => changeYear(1));
    parentElement.querySelector("#btnCurrent").addEventListener("click", () => {
        currentYear = new Date().getFullYear();
        renderTable(currentYear);
    });
    renderTable(currentYear);
}