import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  className?: string
  disabled?: boolean
  onClick?: () => void
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, className, disabled, onClick, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            className={className}
            disabled={disabled}
            onClick={onClick}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            {damage && <p className="text-sm">Damage: {damage}</p>}
            {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
