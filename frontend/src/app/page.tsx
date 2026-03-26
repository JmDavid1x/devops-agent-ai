import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { DashboardLayout } from "@/components/dashboard-layout";
import {
  Server,
  Container,
  AlertTriangle,
  Rocket,
  Play,
  RefreshCw,
  Terminal,
} from "lucide-react";

const stats = [
  {
    title: "Services Up",
    value: "12",
    description: "of 14 total",
    icon: Server,
  },
  {
    title: "Active Containers",
    value: "23",
    description: "across 3 hosts",
    icon: Container,
  },
  {
    title: "Recent Alerts",
    value: "3",
    description: "last 24 hours",
    icon: AlertTriangle,
  },
  {
    title: "Deployments Today",
    value: "5",
    description: "all successful",
    icon: Rocket,
  },
];

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6 p-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              DevOps AI Agent
            </h1>
            <p className="text-sm text-muted-foreground">
              Infrastructure overview and management
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex size-2.5">
              <span className="absolute inline-flex size-full animate-ping rounded-full bg-green-400 opacity-75" />
              <span className="relative inline-flex size-2.5 rounded-full bg-green-500" />
            </span>
            <Badge variant="outline">System Online</Badge>
          </div>
        </div>

        <Separator />

        {/* Stats Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <Card key={stat.title}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardDescription>{stat.title}</CardDescription>
                    <Icon className="size-4 text-muted-foreground" />
                  </div>
                  <CardTitle className="text-2xl">{stat.value}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground">
                    {stat.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div>
          <h2 className="mb-3 text-lg font-semibold">Quick Actions</h2>
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" size="sm">
              <Play className="size-3.5" />
              Deploy Service
            </Button>
            <Button variant="outline" size="sm">
              <RefreshCw className="size-3.5" />
              Restart Container
            </Button>
            <Button variant="outline" size="sm">
              <Terminal className="size-3.5" />
              Open Terminal
            </Button>
            <Button variant="outline" size="sm">
              <AlertTriangle className="size-3.5" />
              View Alerts
            </Button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
