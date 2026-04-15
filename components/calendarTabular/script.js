export default function (component) {
	const { parentElement, data, setTriggerValue } = component;

	const feriadosCache = {};
	const tableHead = parentElement.querySelector("#tableHead");
	const tableBody = parentElement.querySelector("#tableBody");
	const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
	const weekDaysShort = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

	let currentMonth = new Date().getMonth();
	let currentYear = new Date().getFullYear();

	function isLeapYear(year) {
		return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
	}

	function getDaysInMonth(month, year) {
		const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
		return (month === 1 && isLeapYear(year)) ? 29 : daysInMonth[month];
	}

	async function fetchFeriados(year) {
		if (feriadosCache[year]) return feriadosCache[year];
		try {
			const res = await fetch(`https://brasilapi.com.br/api/feriados/v1/${year}`);
			const list = await res.json();
			const map = {};
			list.forEach(f => { map[f.date] = f.name; });
			feriadosCache[year] = map;
			return map;
		} catch {
			feriadosCache[year] = {};
			return {};
		}
	}

	async function renderTable(month, year) {
		const feriados = await fetchFeriados(year);
		const numDays = getDaysInMonth(month, year);
		const today = new Date();
		today.setHours(0, 0, 0, 0);

		let headerHTML = `<tr><th class="col-fixed">Obras</th>`;

		for (let d = 1; d <= numDays; d++) {
			const dateObj = new Date(year, month, d);
			const dayOfWeek = weekDaysShort[dateObj.getDay()];
			const dayIndex = dateObj.getDay();
			const dateString = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;

			const isToday = (dateObj.getTime() === today.getTime());
			const isWeekend = (dayIndex === 0 || dayIndex === 6);
			const isFeriado = !!feriados[dateString];
			const feriadoNome = feriados[dateString] || "";

			const classes = [
				"col-day",
				isWeekend ? "is-weekend" : "",
				isToday ? "is-today-col" : "",
				isFeriado ? "is-holiday" : ""
			].filter(Boolean).join(" ");

			const titleAttr = isFeriado ? `title="${feriadoNome}"` : "";

			headerHTML += `
		<th class="${classes}" ${titleAttr}>
			<div class="th-content">
				<span class="th-day-week">${dayOfWeek}</span>
				<span class="th-day-num">${d}</span>
				${isFeriado ? `<span class="th-holiday-dot"></span>` : ""}
			</div>
		</th>
		`;
		}

		headerHTML += `
		<th class="col-summary">
			<div class="th-content">
				<span class="th-day-week">Não</span>
				<span class="th-day-num">Env.</span>
			</div>
		</th>`;

		headerHTML += `</tr>`;
		tableHead.innerHTML = headerHTML;
		tableBody.innerHTML = "";

		const dadosFiltrados = data.filter(item => {
			const [y, m] = item.date_in.split('-').map(Number);
			return (m - 1) === month && y === year;
		});
		const projetos = [...new Set(dadosFiltrados.map(item => item.obra))];

		projetos.forEach(projeto => {
			const dadosFiltro = dadosFiltrados
				.filter(item => item.obra === projeto)
				.map(item => item.date_in);
			const cellName = document.createElement("td");
			const row = document.createElement("tr");
			cellName.classList.add("col-fixed");
			cellName.textContent = projeto;
			row.appendChild(cellName);

			let naoEnviadoCount = 0;

			for (let d = 1; d <= numDays; d++) {
				const cell = document.createElement("td");
				const dateString = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
				const cellDate = new Date(year, month, d);
				const dayIndex = cellDate.getDay();
				const isWeekend = (dayIndex === 0 || dayIndex === 6);
				const isFeriado = !!feriados[dateString];

				if (isWeekend) cell.classList.add("is-weekend");
				if (isFeriado) cell.classList.add("is-holiday");
				if (cellDate.getTime() === today.getTime()) cell.classList.add("is-today-col");

				if (cellDate <= today) {
					const status = dadosFiltro.includes(dateString) ? 'check' : 'x';
	
					if (status === 'x' && !isWeekend && !isFeriado)
						naoEnviadoCount++;

					const iconDiv = document.createElement("div");
					iconDiv.classList.add(status);

					const svgIcon = status === 'check'
						? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
						: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';

					iconDiv.innerHTML = `<div class="icon-box">${svgIcon}</div>`;
					cell.appendChild(iconDiv);
				}
				row.appendChild(cell);
			}

			const summaryCell = document.createElement("td");
			summaryCell.classList.add("col-summary");
			summaryCell.innerHTML = `<span class="summary-badge ${naoEnviadoCount === 0 ? 'summary-badge--zero' : ''}">${naoEnviadoCount}</span>`;
			row.appendChild(summaryCell);

			tableBody.appendChild(row);
		});

		parentElement.querySelector("#nextMonth").disabled = (year > today.getFullYear() || (year === today.getFullYear() && month >= today.getMonth()));
		parentElement.querySelector("#monthYear").textContent = monthNames[month] + " " + year;
		setTriggerValue('clicked', `${month + 1}-${year}`);
	}

	async function changeMonth(offset) {
		currentMonth += offset;
		if (currentMonth < 0) {
			currentMonth = 11;
			currentYear--;
		} else if (currentMonth > 11) {
			currentMonth = 0;
			currentYear++;
		}
		await renderTable(currentMonth, currentYear);
	}

	parentElement.querySelector("#prevMonth").addEventListener("click", () => changeMonth(-1));
	parentElement.querySelector("#nextMonth").addEventListener("click", () => changeMonth(1));
	parentElement.querySelector("#today").addEventListener("click", () => {
		const now = new Date();
		currentMonth = now.getMonth();
		currentYear = now.getFullYear();
		renderTable(currentMonth, currentYear);
	});

	renderTable(currentMonth, currentYear);
}