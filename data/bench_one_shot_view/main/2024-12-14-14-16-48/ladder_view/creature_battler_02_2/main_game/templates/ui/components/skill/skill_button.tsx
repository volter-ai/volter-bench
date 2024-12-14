import * as React from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  skillName: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, className, skillName, description, stats, ...props }, ref) => {
    return (
      <div className="space-y-2">
        <Button
          ref={ref}
          className={cn("w-[200px]", className)}
          {...props}
        >
          {skillName}
        </Button>
        <div className="absolute z-50 hidden group-hover:block w-80 rounded-md border bg-popover p-4 text-popover-foreground shadow-md">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            <div className="flex gap-4 text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.type && <div>Type: {stats.type}</div>}
            </div>
          </div>
        </div>
      </div>
    )
  }
)

SkillButton.displayName = "SkillButton"

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
