import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent, CardProps } from "@/components/ui/card"

interface CreatureCardProps extends CardProps {
  uid: string;
  name: string;
  image: string;
  hp: number;
  maxHp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, hp, maxHp, ...props }, ref) => (
    <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={image} alt={name} className="w-full h-40 object-cover mb-4" />
        <div className="flex justify-between items-center">
          <span>HP:</span>
          <span>{hp}/{maxHp}</span>
        </div>
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
