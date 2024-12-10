import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

interface CreatureSubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CreatureCardBase = Card
let CreatureCardHeaderBase = CardHeader
let CreatureCardTitleBase = CardTitle
let CreatureCardContentBase = CardContent

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardBase uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeaderBase uid={`${uid}-header`}>
          <CreatureCardTitleBase uid={`${uid}-title`}>{name}</CreatureCardTitleBase>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CreatureCardHeaderBase>
        <CreatureCardContentBase uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CreatureCardContentBase>
      </CreatureCardBase>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCardBase = withClickable(CreatureCardBase)
CreatureCardHeaderBase = withClickable(CreatureCardHeaderBase)
CreatureCardTitleBase = withClickable(CreatureCardTitleBase)
CreatureCardContentBase = withClickable(CreatureCardContentBase)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
