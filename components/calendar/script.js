export default function (component) {
  const { parentElement, data, setTriggerValue } = component;

  console.log("Calendar component initialized with data:", data);

  const tableBodyCalendar = parentElement.querySelector("#calendarBody");
  const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
  const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  const atividades = data || {};

  let currentMonth = new Date().getMonth();
  let currentYear = new Date().getFullYear();

  function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  }

  function renderCalendar(month, year) {
    tableBodyCalendar.innerHTML = "";
    const firstDay = new Date(year, month).getDay();
    let daysInCurrentMonth = daysInMonth[month];
    if (month === 1 && isLeapYear(year)) {
      daysInCurrentMonth = 29;
    }

    let date = 1;
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (let i = 0; i < 6; i++) {
      const row = document.createElement("tr");
      let hasDays = false;

      for (let j = 0; j < 7; j++) {
        const cell = document.createElement("td");

        if (i === 0 && j < firstDay) {
          row.appendChild(cell);
        } else if (date > daysInCurrentMonth) {
          row.appendChild(cell);
        } else {
          hasDays = true;
          const dateString = `${year}-${String(month + 1).padStart(2, "0")}-${String(date).padStart(2, "0")}`;
          const cellDate = new Date(year, month, date);

          const numberSpan = document.createElement("span");
          numberSpan.textContent = date;
          numberSpan.classList.add("day-number");
          cell.appendChild(numberSpan);

          if (cellDate < today) {
            const isChecked = atividades[dateString] === 'check';
            const statusType = isChecked ? 'check' : 'x';

            const iconDiv = document.createElement("div");
            iconDiv.classList.add("status-icon", statusType);

            const svgIcon = statusType === 'check'
              ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
              : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';

            iconDiv.innerHTML = `<div class="icon-box">${svgIcon}</div>`;
            cell.appendChild(iconDiv);
          }

          if (cellDate.getTime() === today.getTime()) {
            cell.classList.add("is-today");
          }

          date++;
          row.appendChild(cell);
        }
      }
      if (hasDays) {
        tableBodyCalendar.appendChild(row);
      }
    }
    parentElement.querySelector("#monthYear").textContent = monthNames[month] + " " + year;
    setTriggerValue('clicked',`${month + 1}-${year}`);
  }

  function changeMonth(offset) {
    currentMonth += offset;
    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
    } else if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }
    renderCalendar(currentMonth, currentYear);
  }

  parentElement.querySelector("#prevMonth").addEventListener("click", () => changeMonth(-1));
  parentElement.querySelector("#nextMonth").addEventListener("click", () => changeMonth(1));

  parentElement.querySelector("#today").addEventListener("click", () => {
    const now = new Date();
    currentMonth = now.getMonth();
    currentYear = now.getFullYear();
    renderCalendar(currentMonth, currentYear);
  });
  renderCalendar(currentMonth, currentYear);
};