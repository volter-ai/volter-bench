import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"

interface CreatureCardProps extends React.ComponentPropsWithoutRef<typeof Card> {
  uid: string;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader>
        <CardTitle>{props.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={props.imageUrl} alt={props.name} className="w-full h-40 object-cover rounded-md" />
      </CardContent>
      <CardFooter>
        <p>HP: {props.hp}</p>
      </CardFooter>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
