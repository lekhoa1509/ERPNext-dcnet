"""
Bench CLI commands for DCNET Fixtures

Usage:
    bench --site [site] dcnet-fixtures generate [OPTIONS]
    bench --site [site] dcnet-fixtures clear [--force]
    bench --site [site] dcnet-fixtures status

Examples:
    # Generate all sample data (master + dynamic Vietnamese data)
    bench --site flow.local dcnet-fixtures generate

    # Generate with custom counts
    bench --site flow.local dcnet-fixtures generate --leads 200 --customers 150

    # Generate specific module only
    bench --site flow.local dcnet-fixtures generate --module fitting --fitting-sessions 100

    # Skip master data (only generate dynamic data)
    bench --site flow.local dcnet-fixtures generate --skip-master

Available modules: master, leads, customers, suppliers, opportunities, sales-orders, purchase-orders, fitting, order-schedule
"""

import click
import frappe
from frappe.commands import pass_context, get_site


@click.group()
def dcnet_fixtures():
    """DCNET Sample Data Fixtures for Golf Business"""
    pass


@dcnet_fixtures.command("generate")
@click.option("--leads", default=150, help="Number of Leads to generate")
@click.option("--opportunities", default=100, help="Number of Opportunities to generate")
@click.option("--customers", default=100, help="Number of Customers to generate")
@click.option("--suppliers", default=50, help="Number of Suppliers to generate")
@click.option("--sales-orders", default=150, help="Number of Sales Orders to generate")
@click.option("--purchase-orders", default=100, help="Number of Purchase Orders to generate")
@click.option("--fitting-sessions", default=50, help="Number of Fitting Sessions to generate")
@click.option("--submit", is_flag=True, help="Submit orders (creates GL entries)")
@click.option("--skip-master", is_flag=True, help="Skip installing master data (Item Groups, Items, etc.)")
@click.option("--module", default=None, help="Generate specific module: master, leads, customers, suppliers, opportunities, sales-orders, purchase-orders, fitting")
@pass_context
def generate_data(context, leads, opportunities, customers, suppliers, sales_orders, purchase_orders, fitting_sessions, submit, skip_master, module):
    """Generate sample data for DCNET Golf Business

    This command will:
    1. Install master data (Item Groups, Items, Warehouses, etc.) from JSON fixtures
    2. Generate dynamic Vietnamese data (Leads, Customers, Orders, Fitting Sessions)

    \b
    Examples:
        bench --site flow.local dcnet-fixtures generate
        bench --site flow.local dcnet-fixtures generate --leads 200 --customers 150
        bench --site flow.local dcnet-fixtures generate --module fitting --fitting-sessions 100
        bench --site flow.local dcnet-fixtures generate --skip-master
    """
    site = get_site(context)

    with frappe.init_site(site):
        frappe.connect()
        try:
            # Handle specific module
            if module:
                if module == "master":
                    # Install master data only
                    click.echo("Installing master data from JSON fixtures...")
                    from dcnet_fixtures.dcnet_fixtures.setup_fixtures import install_module
                    install_module("master")
                    click.echo(click.style("Master data installed!", fg="green"))
                else:
                    # Generate specific dynamic module
                    _generate_module(module, leads, opportunities, customers, suppliers,
                                   sales_orders, purchase_orders, fitting_sessions, submit)
            else:
                # Full generation: master + all dynamic data
                if not skip_master:
                    click.echo("\n[Step 1] Installing master data from JSON fixtures...")
                    _install_master_data()

                click.echo("\n[Step 2] Generating Vietnamese sample data...")
                from dcnet_fixtures.dcnet_fixtures.generators.vietnamese_data import generate_all_data

                result = generate_all_data(
                    leads=leads,
                    opportunities=opportunities,
                    customers=customers,
                    suppliers=suppliers,
                    sales_orders=sales_orders,
                    purchase_orders=purchase_orders,
                    fitting_sessions=fitting_sessions,
                    submit_orders=submit
                )
                click.echo(click.style("\nAll data generated successfully!", fg="green"))

            frappe.db.commit()
        except Exception as e:
            frappe.db.rollback()
            click.echo(click.style(f"Error: {str(e)}", fg="red"))
            raise
        finally:
            frappe.destroy()


def _install_master_data():
    """Install master data from JSON fixtures if not already present"""
    from dcnet_fixtures.dcnet_fixtures.setup_fixtures import install_module, get_fixtures_status

    status = get_fixtures_status()

    # Check if master data already exists
    master_count = sum(status.get("master", {}).values())

    if master_count > 0:
        click.echo(f"  Master data already exists ({master_count} records). Skipping...")
    else:
        click.echo("  Installing master data (Item Groups, Items, Warehouses)...")
        install_module("master")
        click.echo(click.style("  Master data installed!", fg="green"))

    frappe.db.commit()


def _generate_module(module, leads, opportunities, customers, suppliers, sales_orders, purchase_orders, fitting_sessions, submit):
    """Generate a specific module"""
    from dcnet_fixtures.dcnet_fixtures.generators.vietnamese_data import (
        generate_leads,
        generate_customers,
        generate_suppliers,
        generate_opportunities,
        generate_sales_orders,
        generate_purchase_orders,
        generate_fitting_sessions
    )

    click.echo(f"Generating {module}...")

    if module == "leads":
        result = generate_leads(leads)
    elif module == "customers":
        result = generate_customers(customers)
    elif module == "suppliers":
        result = generate_suppliers(suppliers)
    elif module == "opportunities":
        result = generate_opportunities(opportunities)
    elif module == "sales-orders":
        result = generate_sales_orders(sales_orders, submit=submit)
    elif module == "purchase-orders":
        result = generate_purchase_orders(purchase_orders, submit=submit)
    elif module == "fitting":
        result = generate_fitting_sessions(fitting_sessions)
    elif module == "order-schedule":
        # Load Order Schedule from JSON fixtures
        from dcnet_fixtures.dcnet_fixtures.setup_fixtures import load_json_file, create_record, FIXTURES_DIR
        json_file = FIXTURES_DIR / "master" / "07_order_schedule.json"
        data = load_json_file(json_file)
        result = []
        for record in data:
            create_record(record)
            result.append(record.get("category_name"))
        click.echo(click.style(f"Loaded {len(result)} Order Schedule records!", fg="green"))
        return
    else:
        click.echo(click.style(f"Unknown module: {module}", fg="red"))
        click.echo("Available: master, leads, customers, suppliers, opportunities, sales-orders, purchase-orders, fitting, order-schedule")
        return

    click.echo(click.style(f"Generated {len(result)} records!", fg="green"))


@dcnet_fixtures.command("clear")
@click.option("--force", is_flag=True, help="Force clear without confirmation")
@pass_context
def clear_fixtures(context, force=False):
    """Clear all sample data fixtures"""
    site = get_site(context)

    if not force:
        click.confirm("This will delete ALL sample data. Are you sure?", abort=True)

    with frappe.init_site(site):
        frappe.connect()
        try:
            from dcnet_fixtures.dcnet_fixtures.setup_fixtures import clear_all_fixtures

            click.echo("Clearing all fixtures...")
            clear_all_fixtures()

            frappe.db.commit()
            click.echo(click.style("All fixtures cleared!", fg="green"))
        except Exception as e:
            frappe.db.rollback()
            click.echo(click.style(f"Error: {str(e)}", fg="red"))
            raise
        finally:
            frappe.destroy()


@dcnet_fixtures.command("status")
@pass_context
def fixtures_status(context):
    """Show current fixtures status"""
    site = get_site(context)

    with frappe.init_site(site):
        frappe.connect()
        try:
            from dcnet_fixtures.dcnet_fixtures.setup_fixtures import get_fixtures_status

            status = get_fixtures_status()

            click.echo("\n" + "=" * 60)
            click.echo("DCNET Fixtures Status")
            click.echo("=" * 60)

            total = 0
            for module, data in status.items():
                module_total = sum(data.values())
                total += module_total
                click.echo(f"\n{module.upper()}:")
                for doctype, count in data.items():
                    color = "green" if count > 0 else "yellow"
                    click.echo(click.style(f"  {doctype}: {count}", fg=color))

            click.echo("\n" + "-" * 60)
            click.echo(f"TOTAL: {total} records")
            click.echo("=" * 60 + "\n")
        finally:
            frappe.destroy()


@dcnet_fixtures.command("generate-3y")
@click.option("--start-year", default=2023, type=int, help="Start year (default: 2023)")
@click.option("--phase", default=None,
              type=click.Choice(["foundation", "accounting", "master", "crm", "stock", "procurement", "sales", "expenses", "all"]),
              help="Run only a specific phase (default: all)")
@click.option("--clear", is_flag=True, help="Clear all sample data before generating")
@click.option("--skip-master", is_flag=True, help="Skip master data phase")
@click.option("--skip-crm", is_flag=True, help="Skip CRM phase")
@click.option("--skip-stock", is_flag=True, help="Skip stock setup")
@click.option("--skip-procurement", is_flag=True, help="Skip procurement cycle")
@click.option("--skip-sales", is_flag=True, help="Skip sales cycle")
@click.option("--skip-expenses", is_flag=True, help="Skip business expenses")
@pass_context
def generate_3y(context, start_year, phase, clear, skip_master, skip_crm, skip_stock, skip_procurement, skip_sales, skip_expenses):
    """Generate 3 years of realistic business data with 50% YoY growth.

    \b
    PHASE ORDER (runs automatically in this order):
        1. foundation  - Fiscal Years, Cost Centers, Warehouses, Tax Templates
        2. master      - Items, Customers, Suppliers
        3. crm         - Leads, Opportunities
        4. stock       - Opening Stock, Quarterly Restocks, Transfers
        5. procurement - PO → Purchase Receipt → Purchase Invoice → Payment
        6. sales       - SO → Delivery Note → Sales Invoice → Payment
        7. expenses    - Monthly Expenses (Rent, Payroll, Marketing...)

    \b
    Full cycle with clearing:
        bench --site flow.local dcnet-fixtures generate-3y --clear

    \b
    Specific phases:
        bench --site flow.local dcnet-fixtures generate-3y --phase stock
    """
    site = get_site(context)

    with frappe.init_site(site):
        frappe.connect()
        try:
            if clear:
                click.echo(click.style("\n[Step 0] Clearing all existing data...", fg="yellow", bold=True))
                from dcnet_fixtures.dcnet_fixtures.setup_fixtures import clear_all_fixtures
                clear_all_fixtures()
                frappe.db.commit()
                click.echo(click.style("  ✅ All fixtures cleared!", fg="green"))

            years = list(range(start_year, 2027))
            click.echo(f"\nGenerating 3-Year Data: {start_year} → 2026 Q1")
            click.echo(f"Years: {years}")
            click.echo("=" * 60)

            # ----------------------------------------------------------------
            # Phase 1: Foundation
            # ----------------------------------------------------------------
            if phase in (None, "all", "foundation"):
                click.echo(click.style("\n[Phase 1] Foundation Setup...", fg="cyan", bold=True))
                from dcnet_fixtures.dcnet_fixtures.generators.foundation import setup_all_foundation
                setup_all_foundation()
                frappe.db.commit()

            # ----------------------------------------------------------------
            # Phase 1.5: Vietnamese Accounting (TT200 + Capital)
            # ----------------------------------------------------------------
            if phase in (None, "all", "accounting"):
                click.echo(click.style("\n[Phase 1.5] Vietnamese Accounting (TT200, Capital, Assets)...", fg="cyan", bold=True))
                from dcnet_fixtures.dcnet_fixtures.generators.vietnamese_accounting import setup_all_vietnamese_accounting
                setup_all_vietnamese_accounting()
                frappe.db.commit()

            # ----------------------------------------------------------------
            # Phase 2: Master
            # ----------------------------------------------------------------
            if phase in (None, "all", "master") and not skip_master:
                click.echo(click.style("\n[Phase 2] Master Data (Items, Customers, Suppliers)...", fg="cyan", bold=True))
                from dcnet_fixtures.dcnet_fixtures.setup_fixtures import install_module
                install_module("master")
                frappe.db.commit()

                from dcnet_fixtures.dcnet_fixtures.generators.vietnamese_data import (
                    generate_customers, generate_suppliers
                )
                generate_customers(count=150, b2b_ratio=0.35)
                generate_suppliers(count=80)
                frappe.db.commit()

            # ----------------------------------------------------------------
            # Phase 3: CRM
            # ----------------------------------------------------------------
            if phase in (None, "all", "crm") and not skip_crm:
                click.echo(click.style("\n[Phase 3] CRM Data (Leads, Opportunities)...", fg="cyan", bold=True))
                from dcnet_fixtures.dcnet_fixtures.generators.vietnamese_data import (
                    generate_leads, generate_opportunities
                )
                generate_leads(count=200)
                generate_opportunities(count=150)
                frappe.db.commit()

            # ----------------------------------------------------------------
            # Phase 4: Stock
            # ----------------------------------------------------------------
            if phase in (None, "all", "stock") and not skip_stock:
                click.echo(click.style("\n[Phase 4] Stock Setup (Opening Stock + Transfers)...", fg="cyan", bold=True))
                from dcnet_fixtures.dcnet_fixtures.generators.stock_management import setup_all_stock
                result = setup_all_stock(years=years)
                frappe.db.commit()
                click.echo(click.style(
                    f"  ✅ Stock: {len(result.get('opening',[]))} opening entries, "
                    f"{result.get('restocks',0)} restocks, "
                    f"{len(result.get('transfers',[]))} transfers",
                    fg="green"
                ))

            # ----------------------------------------------------------------
            # Phase 5: Procurement Cycle
            # ----------------------------------------------------------------
            if phase in (None, "all", "procurement") and not skip_procurement:
                click.echo(click.style("\n[Phase 5] Procurement Cycle (PO→PR→PI→Payment)...", fg="cyan", bold=True))
                click.echo("  This may take several minutes...")
                from dcnet_fixtures.dcnet_fixtures.generators.procurement import generate_procurement_3y
                result = generate_procurement_3y(years=years)
                frappe.db.commit()
                click.echo(click.style(
                    f"  ✅ Procurement: {result.get('purchase_orders',0)} POs, "
                    f"{result.get('purchase_receipts',0)} PRs, "
                    f"{result.get('purchase_invoices',0)} PIs, "
                    f"{result.get('payments',0)} Payments",
                    fg="green"
                ))

            # ----------------------------------------------------------------
            # Phase 6: Sales Cycle
            # ----------------------------------------------------------------
            if phase in (None, "all", "sales") and not skip_sales:
                click.echo(click.style("\n[Phase 6] Sales Cycle (SO→DN→SI→Payment)...", fg="cyan", bold=True))
                click.echo("  This may take several minutes...")
                from dcnet_fixtures.dcnet_fixtures.generators.sales_cycle import generate_sales_3y
                result = generate_sales_3y(years=years)
                frappe.db.commit()
                click.echo(click.style(
                    f"  ✅ Sales: {result.get('sales_orders',0)} SOs, "
                    f"{result.get('delivery_notes',0)} DNs, "
                    f"{result.get('sales_invoices',0)} SIs, "
                    f"{result.get('payments',0)} Payments",
                    fg="green"
                ))

            # ----------------------------------------------------------------
            # Phase 7: Business Expenses
            # ----------------------------------------------------------------
            if phase in (None, "all", "expenses") and not skip_expenses:
                click.echo(click.style("\n[Phase 7] Business Expenses (Rent, Payroll, Marketing...)...", fg="cyan", bold=True))
                from dcnet_fixtures.dcnet_fixtures.generators.business_expenses import generate_expenses_3y
                result = generate_expenses_3y(years=years)
                frappe.db.commit()
                click.echo(click.style(
                    f"  ✅ Expenses: {result.get('created',0)} journal entries",
                    fg="green"
                ))

            frappe.db.commit()
            click.echo(click.style("\n✅ 3-Year Data Generation Complete!", fg="green", bold=True))
            click.echo("Run 'bench --site flow.local dcnet-fixtures status' to check record counts.")

        except Exception as e:
            frappe.db.rollback()
            click.echo(click.style(f"\n❌ Error: {str(e)}", fg="red"))
            import traceback
            traceback.print_exc()
            raise
        finally:
            frappe.destroy()


# Register commands with Frappe
commands = [dcnet_fixtures]
