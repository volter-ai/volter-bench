import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  hp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, name, image, hp, maxHp, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("creature-card", className)} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={image} alt={`${name} image`} className="creature-image" />
        <div className="hp-bar">
          <div
            className="hp-bar-fill"
            style={{ width: `${(hp / maxHp) * 100}%` }}
          />
        </div>
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
