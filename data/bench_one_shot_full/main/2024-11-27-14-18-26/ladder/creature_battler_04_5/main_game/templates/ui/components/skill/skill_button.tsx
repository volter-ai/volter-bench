import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
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
            className="w-full h-full"
            uid={`${uid}-button`}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="font-medium">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="grid grid-cols-3 gap-4">
              {damage !== undefined && (
                <div className="text-sm">
                  <div className="font-medium">Damage</div>
                  <div>{damage}</div>
                </div>
              )}
              {accuracy !== undefined && (
                <div className="text-sm">
                  <div className="font-medium">Accuracy</div>
                  <div>{accuracy}%</div>
                </div>
              )}
              {cost !== undefined && (
                <div className="text-sm">
                  <div className="font-medium">Cost</div>
                  <div>{cost}</div>
                </div>
              )}
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
