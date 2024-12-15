import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  pp?: number
  className?: string
  onClick?: () => void
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, pp, className, onClick, ...props }, ref) => {
    return (
      <HoverCard>
        <HoverCardTrigger asChild>
          <Button
            ref={ref}
            uid={`${uid}-button`}
            onClick={onClick}
            className={className}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            {damage && <p className="text-sm">Damage: {damage}</p>}
            {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
            {pp && <p className="text-sm">PP: {pp}</p>}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
