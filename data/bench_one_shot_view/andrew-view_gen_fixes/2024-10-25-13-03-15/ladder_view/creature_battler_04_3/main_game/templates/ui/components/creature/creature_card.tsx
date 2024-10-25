import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
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
        <Progress value={(hp / maxHp) * 100} className="w-full" />
      </CardContent>
      <CardFooter>
        <p className="text-sm">HP: {hp}/{maxHp}</p>
      </CardFooter>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
