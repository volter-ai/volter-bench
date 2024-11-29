import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as ShadcnCard, CardContent as ShadcnCardContent, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

let Card = withClickable(ShadcnCard)
let CardContent = withClickable(ShadcnCardContent)
let CardHeader = withClickable(ShadcnCardHeader)
let CardTitle = withClickable(ShadcnCardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <div className="text-sm">
            HP: {hp}/{maxHp}
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
