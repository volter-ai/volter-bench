import * as React from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  skillName: string
  description: string
  damage?: number
  accuracy?: number
  cost?: number
}

let HoverCardRoot = withClickable(({ uid, children, ...props }: { uid: string, children: React.ReactNode }) => (
  <div {...props}>{children}</div>
))

let HoverCardTrigger = withClickable(({ uid, children, ...props }: { uid: string, children: React.ReactNode }) => (
  <div {...props}>{children}</div>
))

let HoverCardContent = withClickable(({ uid, children, className, ...props }: { uid: string, children: React.ReactNode, className?: string }) => (
  <div className={cn(
    "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md",
    className
  )} {...props}>
    {children}
  </div>
))

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, className, skillName, description, damage, accuracy, cost, ...props }, ref) => {
    return (
      <HoverCardRoot uid={uid}>
        <HoverCardTrigger uid={uid}>
          <Button
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            <div className="flex gap-4 text-sm text-muted-foreground">
              {damage && <div>Damage: {damage}</div>}
              {accuracy && <div>Accuracy: {accuracy}%</div>}
              {cost && <div>Cost: {cost}</div>}
            </div>
          </div>
        </HoverCardContent>
      </HoverCardRoot>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
