import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  cost?: number
}

let BaseSkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, cost, className, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <Button
            uid={uid}
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            <div className="flex gap-4 text-sm">
              {damage && <div>Damage: {damage}</div>}
              {accuracy && <div>Accuracy: {accuracy}%</div>}
              {cost && <div>Cost: {cost}</div>}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

BaseSkillButton.displayName = "BaseSkillButton"

let SkillButton = withClickable(BaseSkillButton)

export { SkillButton }
