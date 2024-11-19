import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  cost?: number
  onClick?: () => void
  disabled?: boolean
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, cost, onClick, disabled, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover-card`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            onClick={onClick}
            disabled={disabled}
            className="w-full h-16"
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-sm">
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

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
