import * as React from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description?: string
  stats?: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, children, description, stats, ...props }, ref) => {
    return (
      <div className={cn("w-[200px]", className)}>
        <Button
          ref={ref}
          uid={uid}
          {...props}
        >
          {children}
          {description && (
            <div className="absolute invisible group-hover:visible bg-popover p-4 rounded-md shadow-md -top-full">
              <p className="text-sm text-muted-foreground">{description}</p>
              {stats && (
                <div className="text-sm">
                  {stats.damage && <p>Damage: {stats.damage}</p>}
                  {stats.accuracy && <p>Accuracy: {stats.accuracy}%</p>}
                  {stats.type && <p>Type: {stats.type}</p>}
                </div>
              )}
            </div>
          )}
        </Button>
      </div>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
